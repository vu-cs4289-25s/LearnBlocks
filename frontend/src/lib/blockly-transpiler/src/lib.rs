use rustpython_parser::{lexer::lex, Mode, parse_tokens, ast};
use malachite_base::strings::ToDebugString;
use malachite_bigint::BigInt;
use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::Mutex;
use unique_id::Generator;
use unique_id::string::StringGenerator;
use wasm_bindgen::prelude::*;

type VariableContainer = Mutex<Lazy<HashMap<String, String>>>;

static VARIABLES_CONTAINER: VariableContainer = Mutex::new(Lazy::new(|| HashMap::new()));
static GEN: Lazy<StringGenerator> = Lazy::new(|| StringGenerator::default());

fn is_reserved_word(keyword: &str) -> Option<&str> {
    match keyword {
        "False" | "None" | "True" | 
        "and" | "as" | "assert" |
        "async" | "await" | "breal" |
        "class" | "continue" | "def" |
        "del" | "elif" | "else" | "except" |
        "finally" | "for" | "from" |
        "global" | "if" | "import" | "in" |
        "is" | "lambda" | "nonlocal" |
        "not" | "or" | "pass" | "raise" |
        "return" | "try" | "while" |
        "with" | "yield" => Some(keyword),
        _ => None
    }
}

fn is_reserved_function(keyword: &str) -> Option<&str> {
    match keyword {
        "print" | "range" | "math" | "round" => Some(keyword),
        _ => None
    }
}

fn insert_next_block(cur: String, insert: String) -> String {
    let next = format!(",\"next\": {{\"block\" : {}}}", insert);
    let mut cur_bytes = Vec::from(cur.as_bytes());
    let mut insert_bytes = Vec::from(next.as_bytes());
    cur_bytes.pop();
    cur_bytes.append(&mut insert_bytes);
    cur_bytes.push(b'}');
    String::from_utf8(cur_bytes).expect("INVALID STRING")
}

fn create_boolean_block(b: bool) -> String {  
    if b {
        format!("{{ \"type\": \"logic_boolean\", \"fields\": {{ \"BOOL\": \"TRUE\" }} }}")
    } else {
        format!("{{ \"type\": \"logic_boolean\", \"fields\": {{ \"BOOL\": \"FALSE\" }} }}")
    }
}

fn create_if_block(test: String, body: String, orelse: Option<String>) -> String {
    if orelse.is_none() {
        let input = format!("{{\"IF0\":{{\"block\":{}}},\"DO0\":{{\"block\":{}}} }}", test, body);
        format!("{{\"type\":\"controls_if\",\"inputs\":{}}}", input)
    } else {
        let input = format!(
            "{{\"IF0\":{{\"block\":{}}},\"DO0\":{{\"block\":{}}},\"ELSE\":{{\"block\":{}}}}}", 
            test, 
            body,
            orelse.unwrap()
        );
        format!(
            "{{\"type\":\"controls_if\",\"inputs\":{},\"extraState\":{{\"hasElse\":\"true\"}}}}", 
            input
        )
    }
}

fn create_compare_block(left: String, ops: Vec<String>, comparators: Vec<String>) -> String {
    if ops.len() == 1 {
        let input = format!(
            "{{\"A\":{{\"block\":{}}},\"B\":{{\"block\":{}}}}}", 
            left, 
            comparators[0].clone()
        );
        let fields = format!("{{\"OP\":\"{}\"}}", ops[0].clone());
        return format!("{{\"type\":\"logic_compare\",\"inputs\":{},\"fields\":{}}}", input, fields);
    }
    format!("{{\"type\":\"logic_compare\"}}")
}

fn create_text_block(text: String) -> String {
    let fields = format!("{{ \"TEXT\": \"{}\" }}", text);
    format!("{{ \"type\": \"text\", \"fields\": {} }}", fields)
}

fn create_float_block(float: f64) -> String {
    format!("{{\"type\":\"math_number\", \"fields\":{{\"NUM\":{}}}}}", float)
}

fn create_int_block(int: &BigInt) -> String {
    format!("{{\"type\":\"math_number\", \"fields\":{{\"NUM\":{}}}}}", int)
}

fn create_bin_op_block(left: String, op: String, right: String) -> String {
    if op.as_str() == "mod" {
        let input = format!(
            "{{\"DIVIDEND\":{{\"block\":{}}},\"DIVISOR\":{{\"block\":{}}}}}", 
            left, 
            right
        );
        format!("{{\"type\":\"math_modulo\",\"inputs\":{}}}", input)
    } else {
        let input = format!("{{\"A\":{{\"block\":{}}},\"B\":{{\"block\":{}}}}}", left, right);
        let fields = format!("{{ \"OP\": \"{}\" }}", op);
        format!("{{\"type\":\"math_arithmetic\",\"inputs\":{},\"fields\":{}}}", input, fields)
    }
}

fn create_bool_op_block(left: String, op: String, right: String) -> String {
    let input = format!("{{\"A\":{{\"block\":{}}},\"B\":{{\"block\":{}}}}}", left, right);
    let fields = format!("{{ \"OP\": \"{}\" }}", op);
    format!("{{\"type\":\"logic_operation\",\"inputs\":{},\"fields\":{}}}", input, fields)
}

fn create_if_exp_block(test: String, body: String, orelse: String) -> String {
    let inputs  = format!(
        "{{\"IF\":{{\"block\":{}}},\"THEN\":{{\"block\":{}}},\"ELSE\":{{\"block\":{}}}}}", 
        test, 
        body, 
        orelse
    );
    format!("{{\"type\":\"logic_ternary\",\"inputs\":{}}}", inputs)
}

fn create_while_block(test: String, body: String) -> String {
    let input = format!("{{\"BOOL\":{{\"block\":{}}},\"DO\":{{\"block\":{}}} }}", test, body);
    format!("{{\"type\":\"controls_whileUntil\",\"inputs\":{}}}", input)
}

fn create_variable_set_block(target: String, value: String) -> String {
    let mut fields = String::from(&target[24..]);
    fields.pop();
    let input = format!("{{\"VALUE\":{{\"block\":{}}}}}", value);
    format!("{{\"type\":\"variables_set\",\"inputs\":{},{}}}", input, fields)
}

fn create_for_range_block(
    target: String, 
    body: String, 
    from: String, 
    to: String, 
    by: String
) -> String {
    let input = format!(
        "{{\"FROM\":{{\"block\":{}}},\"TO\":{{\"block\":{}}},\"DO\":{{\"block\":{}}}, \"BY\":{{\"block\":{}}}}}", 
        from,
        to,
        body,
        by
    );
    format!("{{\"type\":\"controls_for\",\"inputs\":{},{}}}", input, target)
}

fn create_for_each_block(target: String, body: String, list: String) -> String {
    let input = format!(
        "{{\"DO\":{{\"block\":{}}}, \"LIST\":{{\"block\":{}}}}}", 
        body,
        list
    );
    format!("{{\"type\":\"controls_forEach\",\"inputs\":{},{}}}", input, target)
}

fn create_change_variable_block(target: String, value: String) -> String {
    let mut fields = String::from(&target[24..]);
    fields.pop();
    let input = format!("{{\"block\":{}}}", value);
    format!(
        "{{\"type\":\"math_change\",\"inputs\":{{\"DELTA\":{}}},{}}}", 
        input, 
        fields
    )
}

fn create_list_block(elst: &Vec<String>) -> String {
    let list_len = elst.len();
    let extra_state = format!("{{\"itemCount\":{}}}", list_len);

    let mut inputs = String::from("");
    for i in 0..list_len {
        let s = format!("\"ADD{}\":{{\"block\":{}}},", i, elst[i]);
        inputs.push_str(s.as_str());
    }
    inputs.pop();

    format!(
        "{{\"type\":\"lists_create_with\",\"inputs\":{{{}}},\"extraState\":{}}}",
        inputs,
        extra_state
    )
}

fn parse_assign(assign_stmt: &ast::StmtAssign) -> Result<String, String> {
    if assign_stmt.targets.len() != 1 {
        return Err(String::from("invalid number of arguments to assignstatement"));
    }
    let target = parse_expr(&assign_stmt.targets[0]);
    let value = parse_expr(&assign_stmt.value);
    if let (Ok(target), Ok(value))  = (target, value) {
        Ok(create_variable_set_block(target, value))
    } else {
        Err(assign_stmt.to_debug_string())
    }
}

fn parse_aug_assign(aug_assign_stmt: &ast::StmtAugAssign) -> Result<String, String> {
    let target = parse_expr(&aug_assign_stmt.target);
    let raw_value = parse_expr(&aug_assign_stmt.value);
    if let (Ok(target), Ok(raw_value))  = (target, raw_value) {
        let value = match aug_assign_stmt.op {
            ast::Operator::Add | ast::Operator::Mult | 
            ast::Operator::Pow | ast::Operator::Mod => raw_value.clone(),
            _ => format!(
                "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"NEG\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}} }}}}",
                raw_value.clone()
            )
        };
        Ok(create_change_variable_block(target, value))
    } else {
        Err(aug_assign_stmt.to_debug_string())
    }
}

fn parse_for(for_stmt: &ast::StmtFor) -> Result<String, String> {
    if for_stmt.orelse.len() > 0 {
        return Err(String::from("does not support else statements in for loops"));
    }

    let target = parse_expr(&for_stmt.target);
    let iter = parse_expr(&for_stmt.iter);
    let body = join_statements(&for_stmt.body);
    if target.is_err() || iter.is_err() || body.is_err() {
        return Err(for_stmt.to_debug_string());
    }

    let mut fields = String::from(&(target?)[24..]);
    fields.pop();

    if let ast::Expr::Call(_) = *for_stmt.iter {
        let binding = iter.unwrap();
        let iter_vec: Vec<_> = binding.split(",-").collect();
        if iter_vec[0] == "range" {
            let from = String::from(iter_vec[1]);
            let to = String::from(iter_vec[2]);
            let by = if iter_vec.len() >= 4 {
                String::from(iter_vec[3])
            } else {
                String::from("{\"type\":\"math_number\",\"fields\":{\"NUM\": 1}}")
            };
            return Ok(create_for_range_block(fields, body?, from, to, by));
        }
    } else if let ast::Expr::Name(_) = *for_stmt.iter {
        let binding = iter.unwrap();
        return Ok(create_for_each_block(fields, body?, binding));
    }

    return Err(for_stmt.to_debug_string());
}

fn parse_while(while_stmt: &ast::StmtWhile) -> Result<String, String> {
    if while_stmt.orelse.len() > 0 {
        return Err(String::from("does not support else statements in while loops"));
    }

    let test = parse_expr(&while_stmt.test);
    let body = join_statements(&while_stmt.body);
    if test.is_err() || body.is_err() {
        return Err(while_stmt.to_debug_string());
    }
    Ok(create_while_block(test.unwrap(), body.unwrap()))
}

fn parse_if(if_stmt: &ast::StmtIf) -> Result<String, String> {
    let test = parse_expr(&if_stmt.test);
    if test.is_err() {
        return Err(if_stmt.to_debug_string());
    }

    let body = join_statements(&if_stmt.body);
    if body.is_err() {
        return Err(if_stmt.to_debug_string());
    }

    if if_stmt.orelse.len() == 0 {
        Ok(create_if_block(test.unwrap(), body.unwrap(), None))
    } else {
        let orelse = join_statements(&if_stmt.orelse);
        if orelse.is_err() {
            Err(if_stmt.to_debug_string())
        } else {
            Ok(create_if_block(test.unwrap(), body.unwrap(), Some(orelse.unwrap())))
        }
    }
}

fn parse_expr_attribute(expr_attribute: &ast::ExprAttribute) -> Result<String, String> {
    let value = parse_expr(&expr_attribute.value);
    let attr = String::from(expr_attribute.attr.as_str());
    if let Ok(value) = value {
        Ok(format!("{}.{}", value, attr))
    } else {
        Err(expr_attribute.to_debug_string())
    }
}

fn parse_expr_bin_op(expr_bin_op: &ast::ExprBinOp) -> Result<String, String> {
    let left = parse_expr(&expr_bin_op.left);
    if left.is_err() {
        return Err(expr_bin_op.to_debug_string());
    }

    let right = parse_expr(&expr_bin_op.right);
    if right.is_err() {
        return Err(expr_bin_op.to_debug_string());
    }

    let op = match expr_bin_op.op {
        ast::Operator::Add => String::from("ADD"),
        ast::Operator::Sub => String::from("MINUS"),
        ast::Operator::Mult => String::from("MULTIPLY"),
        ast::Operator::Div => String::from("DIVIDE"),
        ast::Operator::Pow => String::from("POWER"),
        ast::Operator::FloorDiv => String::from("DIVIDE"),
        ast::Operator::Mod => String::from("mod"),
        _ => String::from("ADD")
    };

    Ok(create_bin_op_block(left.unwrap(), op, right.unwrap()))
}

fn parse_expr_bool_op(expr_bool_op: &ast::ExprBoolOp) -> Result<String, String> {
    let op = match expr_bool_op.op {
        ast::BoolOp::And => String::from("AND"),
        ast::BoolOp::Or => String::from("OR")
    };

    if expr_bool_op.values.len() < 2 {
        return Err(expr_bool_op.to_debug_string());
    }
    let left = parse_expr(&expr_bool_op.values[0]);
    let right = parse_expr(&expr_bool_op.values[1]);
    
    Ok(create_bool_op_block(left.unwrap(), op, right.unwrap()))
}

fn parse_expr_call(expr_call: &ast::ExprCall) -> Result<String, String> {
    let name = parse_expr(&expr_call.func);
    if name.is_err() {
        return Err(expr_call.to_debug_string());
    }

    let args: Vec<_> = expr_call.args
                                .clone()
                                .into_iter()
                                .map(|expr| parse_expr(&expr))
                                .collect();
    for item in &args {
        if item.is_err() {
            return Err(expr_call.to_debug_string());
        }
    }

    match name.clone().unwrap().as_str() {
        "print" => {
            let input = format!("{{ \"TEXT\" : {{ \"block\" : {} }} }}", args[0].clone().unwrap());
            Ok(format!("{{ \"type\": \"text_print\", \"inputs\": {} }}", input))
        },
        "range" => {
            if args.len() >= 3 {
                return Ok(
                    format!(
                        "range,-{},-{},-{}", 
                        args[0].clone().unwrap(), 
                        args[1].clone().unwrap(),
                        args[2].clone().unwrap()
                    )
                );
            }
            Ok(format!("range,-{},-{}", args[0].clone().unwrap(), args[1].clone().unwrap()))
        },
        "math.sin" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"SIN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.cos" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"COS\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.tan" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"TAN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.asin" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"ASIN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.acos" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"ACOS\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.atan" => {
            Ok(
                format!(
                    "{{\"type\":\"math_trig\",\"fields\":{{\"OP\":\"ATAN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.sqrt" => {
            Ok(
                format!(
                    "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"ROOT\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.fabs" | "math.abs" => {
            Ok(
                format!(
                    "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"ABS\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.log" => {
            Ok(
                format!(
                    "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"LN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.log10" => {
            Ok(
                format!(
                    "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"LOG10\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.exp" => {
            Ok(
                format!(
                    "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"EXP\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "round" => {
            Ok(
                format!(
                    "{{\"type\":\"math_round\",\"fields\":{{\"OP\":\"ROUND\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.ceil" => {
            Ok(
                format!(
                    "{{\"type\":\"math_round\",\"fields\":{{\"OP\":\"ROUNDUP\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        },
        "math.floor" => {
            Ok(
                format!(
                    "{{\"type\":\"math_round\",\"fields\":{{\"OP\":\"ROUNDDOWN\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}}}}}}",
                    args[0].clone().unwrap()
                )
            )
        }
        _ => Ok(String::from(format!("{}", args.to_debug_string())))
    }
}

fn parse_expr_compare(expr_compare: &ast::ExprCompare) -> Result<String, String> {
    let left = parse_expr(&expr_compare.left);
    if left.is_err() {
        return Err(expr_compare.to_debug_string());
    }

    let match_op = |op: ast::CmpOp| -> String {
        match op {
            ast::CmpOp::Eq => String::from("EQ"),
            ast::CmpOp::NotEq => String::from("NEQ"),
            ast::CmpOp::Lt => String::from("LT"),
            ast::CmpOp::LtE => String::from("LTE"),
            ast::CmpOp::Gt => String::from("GT"),
            ast::CmpOp::GtE => String::from("GTE"),
            _ => String::from("NEQ")
        }
    };

    let ops: Vec<_> = expr_compare.ops.clone()
                                      .into_iter()
                                      .map(|op| match_op(op))
                                      .collect();

    let comparators_res: Vec<Result<_, _>> = expr_compare.comparators.clone()
                                                                     .into_iter()
                                                                     .map(|expr| parse_expr(&expr))
                                                                     .collect();
    let comparators: Result<Vec<_>,_> = comparators_res.into_iter().collect();
    if comparators.is_err() {
        return Err(expr_compare.to_debug_string());
    }

    Ok(create_compare_block(left.unwrap(), ops, comparators.unwrap()))
}

fn parse_expr_const(expr_const: &ast::ExprConstant) -> Result<String, String> {
    let value = &expr_const.value;
    match value {
        ast::Constant::Bool(c) => Ok(create_boolean_block(*c)),
        ast::Constant::Str(c) => Ok(create_text_block(c.clone())),
        ast::Constant::Int(c) => Ok(create_int_block(c)),
        ast::Constant::Float(c) => Ok(create_float_block(*c)),
        ast::Constant::None => Ok(String::from("{\"type\":\"logic_null\"}")),
        _ => Err(value.to_debug_string())
    }
}

fn parse_expr_if_exp(expr_if_exp: &ast::ExprIfExp) -> Result<String, String> {
    let test = parse_expr(&expr_if_exp.test);
    let body = parse_expr(&expr_if_exp.body);
    let orelse = parse_expr(&expr_if_exp.orelse);
    if test.is_err() || body.is_err() || orelse.is_err() {
        return Err(expr_if_exp.to_debug_string());
    }
    Ok(create_if_exp_block(test.unwrap(), body.unwrap(), orelse.unwrap()))
}

fn parse_expr_list(expr_list: &ast::ExprList) -> Result<String, String> {
    let elts = expr_list.elts.clone()
                             .into_iter()
                             .map(|e| parse_expr(&e))
                             .filter_map(Result::ok)
                             .collect();
    Ok(create_list_block(&elts))
}

fn parse_expr_name(expr_name: &ast::ExprName) -> Result<String, String> {
    let identifier = expr_name.id.as_str();
    if is_reserved_word(identifier).is_none() && is_reserved_function(identifier).is_none() {
        let mut vars = VARIABLES_CONTAINER.lock().unwrap();
        if vars.get(identifier.into()).is_none() {
            let id = GEN.next_id();
            vars.insert(String::from(identifier), id);
        }
        let id = vars.get(identifier.into());
        return Ok(
            format!(
                "{{\"type\":\"variables_get\",\"fields\":{{\"VAR\":{{\"id\":\"{}\"}}}}}}", 
                id.unwrap()
            )
        );
    }
    return Ok(String::from(identifier));
}

fn parse_expr_unary_op(expr_unary_op: &ast::ExprUnaryOp) -> Result<String, String> {
    let operand = parse_expr(&expr_unary_op.operand);
    if operand.is_err() {
        return Err(expr_unary_op.to_debug_string())
    }

    if let ast::UnaryOp::Not = expr_unary_op.op {
        let input = format!("{{\"BOOL\":{{\"block\":{}}}}}", operand.unwrap());
        Ok(format!("{{\"type\":\"logic_negate\",\"inputs\": {}}}", input))
    } else if let ast::UnaryOp::USub = expr_unary_op.op {
        Ok(
            format!(
                "{{\"type\":\"math_single\",\"fields\":{{\"OP\":\"NEG\"}},\"inputs\":{{\"NUM\":{{\"block\":{}}} }}}}",
                operand.unwrap()
            )
        )
    } else {
        Err(expr_unary_op.to_debug_string())
    }
}

fn parse_expr(expr: &ast::Expr) -> Result<String, String> {
    match expr {
        ast::Expr::Attribute(expr_attribute) => parse_expr_attribute(&expr_attribute),
        ast::Expr::BinOp(expr_bin_op) => parse_expr_bin_op(&expr_bin_op),
        ast::Expr::BoolOp(expr_bool_op) => parse_expr_bool_op(&expr_bool_op),
        ast::Expr::Call(expr_call) => parse_expr_call(&expr_call),
        ast::Expr::Compare(expr_compare) => parse_expr_compare(&expr_compare),
        ast::Expr::Constant(expr_const) => parse_expr_const(&expr_const),
        ast::Expr::IfExp(expr_if_exp) => parse_expr_if_exp(&expr_if_exp),
        ast::Expr::List(expr_list) => parse_expr_list(&expr_list),
        ast::Expr::Name(expr_name) => parse_expr_name(&expr_name),
        ast::Expr::UnaryOp(expr_unary_op) => parse_expr_unary_op(&expr_unary_op),
        _ => Err(expr.to_debug_string())
    }
}

fn parse_statement(stmt: &ast::Stmt) -> Result<String, String> {
    match stmt {
        ast::Stmt::FunctionDef(_) => Ok(String::from("{function def}")),
        ast::Stmt::Return(_) => Ok(String::from("{return def}")),
        ast::Stmt::Delete(_) => Ok(String::from("{delete}")),
        ast::Stmt::Assign(s) => parse_assign(&s),
        ast::Stmt::AugAssign(s) => parse_aug_assign(&s),
        ast::Stmt::AnnAssign(_) => Ok(String::from("{ann assign}")),
        ast::Stmt::For(s) => parse_for(&s),
        ast::Stmt::While(s) => parse_while(&s),
        ast::Stmt::If(s) => parse_if(&s),
        ast::Stmt::With(_) => Ok(String::from("{with}")),
        ast::Stmt::Match(_) => Ok(String::from("{match}")),
        ast::Stmt::Raise(_) => Ok(String::from("{raise}")),
        ast::Stmt::Expr(s) => parse_expr(&s.value),
        ast::Stmt::Pass(_) => Ok(String::from("{pass}")),
        ast::Stmt::Break(_) => Ok(String::from("{pass}")),
        ast::Stmt::Continue(_) => Ok(String::from("{continue}")),
        _ => Err(String::from("unknown statement"))
    }
}

fn join_statements(stmts: &Vec<ast::Stmt>) -> Result<String, String> {
    let raw_proc_stmts: Vec<_> = stmts.into_iter()
                                      .map(|stmt| parse_statement(&stmt))
                                      .collect();
    let res: Result<Vec<_>, _> = raw_proc_stmts.into_iter().collect();
    if res.is_err() {
        return Err(res.to_debug_string());
    }
    let mut proc_stmts = res.unwrap();
    
    if proc_stmts.len() == 1 {
        return Ok(proc_stmts[0].clone())
    }

    proc_stmts.reverse();
    let mut joined = proc_stmts[0].clone();
    for i in 1..proc_stmts.len() {
        joined = insert_next_block(proc_stmts[i].clone(), joined);
    }
    
    Ok(joined)
}

fn create_syntax_tree(python_source: &str) -> Result<ast::Mod, &'static str> {
    let tokens = lex(python_source, Mode::Module);
    let ast = parse_tokens(tokens, Mode::Module, "<embedded>");
    if ast.is_ok() {
        Ok(ast.unwrap())
    } else {
        Err("not valid python")
    }
}

fn create_json_wrappers(blocks: String) -> String {
    let interior_blocks = format!("{{\"blocks\":[{}]}}", blocks);
    let variables = VARIABLES_CONTAINER.lock().unwrap().clone();
    let var_names: Vec<String> = variables.clone().into_keys().collect();
    let var_ids: Vec<String> = variables.into_values().collect();

    let mut var_str = String::from("[");
    for (name, id) in var_names.into_iter().zip(var_ids.into_iter()) {
        let s = format!("{{\"name\": \"{}\", \"id\": \"{}\"}},", name, id);
        var_str.push_str(s.as_str());
    }
    var_str.pop();
    var_str.push(']');

    if var_str.len() == 1 {
        format!("{{\"blocks\":{}}}", interior_blocks)
    } else {
        format!("{{\"blocks\":{}, \"variables\": {} }}", interior_blocks, var_str)
    }
}

fn reset_vars() {
    let mut vars = VARIABLES_CONTAINER.lock().unwrap();
    vars.clear();
}

#[wasm_bindgen]
pub fn ptob_wasm(python_source: &str) -> String {
    reset_vars();
    let raw_ast = create_syntax_tree(python_source);
    if raw_ast.is_ok() {
        let processed_ast = raw_ast.clone().unwrap();
        let raw_module = processed_ast.as_module();
        if raw_module.is_some() {
            let stmts = join_statements(&raw_module.unwrap().body);
            if stmts.is_ok() {
                return create_json_wrappers(stmts.unwrap());
            } else {
                return format!(
                    "{{\"error\": \"cannot parse\", \"details\": {}}}", 
                    stmts.to_debug_string()
                );
            }
        }
    }
    return format!(
        "{{\"error\": \"issue with ast\", \"details\": {}}}",
        raw_ast.to_debug_string()
    );
}