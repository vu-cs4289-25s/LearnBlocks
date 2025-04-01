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
    let vars = VARIABLES_CONTAINER.lock().unwrap();
    let binding = String::from("");
    let var_id = vars.get(&target).unwrap_or(&binding);
    let input = format!("{{\"VALUE\":{{\"block\":{}}}}}", value);
    let fields = format!("{{ \"VAR\": \"{}\"}}", var_id);
    drop(vars);
    format!("{{\"type\":\"variable_set\",\"inputs\":{},\"fields\":{}}}", input, fields)
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

    if name.unwrap().as_str() == "print" {
        let text_block = if args.len() == 0 {
            create_text_block(String::from("\' \'"))
        } else {
            create_text_block(args[0].clone().unwrap())
        };
        let input = format!("{{ \"TEXT\" : {{ \"block\" : {} }} }}", text_block);
        return Ok(format!("{{ \"type\": \"text_print\", \"inputs\": {} }}", input));
    }

    Ok(String::from(format!("{}", args.to_debug_string())))
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
        ast::Constant::Str(c) => Ok(c.clone()),
        ast::Constant::Int(c) => Ok(create_int_block(c)),
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

fn parse_expr_name(expr_name: &ast::ExprName) -> Result<String, String> {
    let identifier = expr_name.id.as_str();
    if is_reserved_word(identifier).is_none() {
        let mut vars = VARIABLES_CONTAINER.lock().unwrap();
        if vars.get(identifier.into()).is_none() {
            let id = GEN.next_id();
            vars.insert(String::from(identifier), id);
        }
        drop(vars);
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
    } else {
        Err(expr_unary_op.to_debug_string())
    }
}

fn parse_expr(expr: &ast::Expr) -> Result<String, String> {
    match expr {
        ast::Expr::BinOp(expr_bin_op) => parse_expr_bin_op(&expr_bin_op),
        ast::Expr::BoolOp(expr_bool_op) => parse_expr_bool_op(&expr_bool_op),
        ast::Expr::Call(expr_call) => parse_expr_call(&expr_call),
        ast::Expr::Compare(expr_compare) => parse_expr_compare(&expr_compare),
        ast::Expr::Constant(expr_const) => parse_expr_const(&expr_const),
        ast::Expr::IfExp(expr_if_exp) => parse_expr_if_exp(&expr_if_exp),
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
        ast::Stmt::AugAssign(_) => Ok(String::from("{aug assign}")),
        ast::Stmt::AnnAssign(_) => Ok(String::from("{ann assign}")),
        ast::Stmt::For(_) => Ok(String::from("{for}")),
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
    format!("{{\"blocks\":{}}}", interior_blocks)
}

#[wasm_bindgen]
pub fn ptob_wasm(python_source: &str) -> String {
    let raw_ast = create_syntax_tree(python_source);
    if raw_ast.is_ok() {
        let processed_ast = raw_ast.unwrap();
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
    return String::from("{ \"error\": \"cannot parse\" }");
}