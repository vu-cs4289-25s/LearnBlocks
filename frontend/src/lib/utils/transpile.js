//LOGIC
function logicCompareHandler(block) {
    const a = parseBlock(block.inputs.A.block);
    const b = parseBlock(block.inputs.B.block);
    let op = '';
    switch (block.fields.OP) {
        case 'EQ':
            op = '==';
            break;
        case 'NEQ':
            op = '!=';
            break;
        case 'LT':
            op = '<';
            break;
        case 'LTE':
            op = '<=';
            break;
        case 'GT':
            op = '>';
            break;
        case 'GTE':
            op = '<=';
            break;
    }
    return `${a} ${op} ${b}`;
}

function logicOperationHandler(block) {
    const a = logicBlockHandler(block.inputs.A.block);
    const b = logicBlockHandler(block.inputs.B.block);
    let op = block.fields.OP === 'AND' ? 'and' : 'or';
    return `${a} ${op} ${b}`;
}

function logicTernaryHandler(block) {
    if (block === undefined) return '';
    if (block.inputs === undefined) return '[a] if [condition] else [b]';
    // TODO
}

function logicBlockHandler(block) {
    if (block === undefined) return '';
    switch (block.type) {
        case 'logic_compare':
            return logicCompareHandler(block);
        case 'logic_operation':
            return logicOperationHandler(block);
        case 'logic_boolean':
            return block.fields.BOOL === 'TRUE' ? 'True' : 'False';
        case 'logic_negate':
            if (block.inputs !== undefined) {
                const logic = logicBlockHandler(block.inputs.BOOL.block);
                return `not ${logic}`;
            }
            return 'not';
        case 'logic_null':
            return 'None'; 
        default:
            return '';
    }
}

function controlIfHandler(block) {
    if (block === undefined) return '';
    if (block.inputs === undefined) return 'if :\n';

    const logicComponent = block.inputs.IF0;
    const nestedComponent = block.inputs.DO0;   
    let code = '';
    
    const logicBlock = logicComponent === undefined ? undefined : logicComponent.block;
    const logicString = logicBlockHandler(logicBlock);
    code += `if ${logicString}:\n`;

    if (nestedComponent !== undefined)
        code += createNestedComponent(nestedComponent.block);

    return code;  
}

//LOOPS

function controlWhileUntilHandler(block) {
    if (block === undefined) return '';
    if (block.inputs === undefined) return 'while :\n';

    const condition = block.inputs.BOOL === undefined ? '' : logicBlockHandler(block.inputs.BOOL.block);
    const mode = block.fields.MODE === 'WHILE' ? 'while' : 'while not';
    let code = `${mode} ${condition}:\n`;

    const nestedComponent = block.inputs.DO;
    if (nestedComponent !== undefined)
        code += createNestedComponent(nestedComponent.block);

    return code;
}

function controlForHandler(block) {
    if (block === undefined) return '';
    if (block.inputs === undefined) return 'for :\n';

    const variableName = SCRIPT_VARIABLES[block.fields.VAR.id];

    const fromBlock = block.inputs.FROM;
    const toBlock = block.inputs.TO;
    const byBlock = block.inputs.BY;

    const rawFrom = fromBlock.block === undefined ? fromBlock.shadow : fromBlock.block;
    const rawTo = toBlock.block === undefined ? toBlock.shadow : toBlock.block;
    const rawBy = byBlock.block === undefined ? byBlock.shadow : byBlock.block;

    const _from = parseBlock(rawFrom);
    const _to = parseBlock(rawTo);
    const _by = parseBlock(rawBy);

    let code = `for ${variableName} in range(${_from}, ${_to}, ${_by}):\n`;

    const nestedComponent = block.inputs.DO;
    if (nestedComponent !== undefined)
        code += createNestedComponent(nestedComponent.block);

    return code;
}

function controlForEachHandler(block) {
    if (block === undefined) return '';
    if (block.inputs === undefined) return 'for :\n';

    const variableName = SCRIPT_VARIABLES[block.fields.VAR.id];
    const list = block.inputs.LIST === undefined ? '' : parseBlock(block.inputs.LIST.block);

    let code = `for ${variableName} in ${list}:\n`;

    const nestedComponent = block.inputs.DO;
    if (nestedComponent !== undefined)
        code += createNestedComponent(nestedComponent.block);

    return code;
}

function controlFlowStatementHandler(block) {
    if (block === undefined) return '';
    switch (block.fields.FLOW) {
        case 'BREAK':
            return 'break\n';
        case 'CONTINUE':
            return 'continue\n';
    }
}

//MATH

function mathArithmeticHandler(block) {
    if (block === undefined) return '';

    let op = '';
    switch(block.fields.OP) {
        case 'ADD':
            op = '+';
            break;
        case 'MINUS':
            op = '-';
            break;
        case 'MULTIPLY':
            op = '*';
            break;
        case 'DIVIDE':
            op = '/';
            break;
        case 'POWER':
            op = '**';
            break;
    }

    const aSlot = block.inputs.A;
    const bSlot = block.inputs.B;

    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);
    const b = parseBlock(bSlot.block === undefined ? bSlot.shadow : bSlot.block);

    return `${a} ${op} ${b}\n`;
}

function mathSingleHandler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.NUM;
    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);


    switch(block.fields.OP) {
        case 'ROOT':
            return `math.sqrt(${a})`;
        case 'ABS':
            return `math.abs(${a})`;
        case 'NEG':
            return `(-1 * ${a})`;
        case 'LN':
            return `math.log(${a})`;
        case 'LOG10':
            return `math.log10(${a})`;
        case 'EXP':
            return `math.exp(${a})`;
        case 'POW10':
            return `10 ** ${a}`;
    }

    return '';
}

function mathTrigHandler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.NUM;
    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);

    switch(block.fields.OP) {
        case 'SIN':
            return `math.sin(${a})`;
        case 'COS':
            return `math.cos(${a})`
        case 'TAN':
            return `math.tan(${a})`;
        case 'ASIN':
            return `math.asin(${a})`;
        case 'ACOS':
            return `math.acos(${a})`
        case 'ATAN':
            return `math.atan(${a})`;
    }

    return '';
}

function mathConstantHandler(block) {
    if (block === undefined) return '';

    switch(block.fields.CONSTANT) {
        case 'PI':
            return 'math.pi';
        case 'E':
            return 'math.e';
        case 'GOLDEN_RATIO':
            return '(1 + math.sqrt(5)) / 2';
        case 'SQRT2':
            return 'math.sqrt(2)';
        case 'SQRT1_2':
            return 'math.sqrt(0.5)';
    }

    return '';
}

function mathRoundHandler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.NUM;
    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);

    switch(block.fields.OP) {
        case 'ROUND':
            return `round(${a})`;
        case 'ROUNDUP':
            return `math.ceil(${a})`;
        case 'ROUNDDOWN':
            return `math.floor(${a})`;
    }

    return '';
}

function mathOnListHandler(block) {
    if (block === undefined) return '';
    // TODO
    return '';
}

function mathModuloHandler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.DIVIDEN;
    const bSlot = block.inputs.DIVISOR;

    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);
    const b = parseBlock(bSlot.block === undefined ? bSlot.shadow : bSlot.block);

    return 'a % b';
}

function mathRandomIntHandler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.FROM;
    const bSlot = block.inputs.TO;

    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);
    const b = parseBlock(bSlot.block === undefined ? bSlot.shadow : bSlot.block);

    return `random.randint(${a}, ${b})`;
}

function mathATan2Handler(block) {
    if (block === undefined) return '';

    const aSlot = block.inputs.X;
    const bSlot = block.inputs.Y;

    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);
    const b = parseBlock(bSlot.block === undefined ? bSlot.shadow : bSlot.block);

    return `math.atan2(${b}, ${a})`;
}

//TEXT

function textHandler(block) {
    if (block === undefined) return '';
    const text = block.fields.TEXT;
    return `'${text}'`;
}

function textAppendHandler(block) {
    if (block === undefined) return '';

    const variableName = SCRIPT_VARIABLES[block.fields.VAR.id];
    const inputBlock = block.inputs.TEXT;
    const input = parseBlock(inputBlock.block ? inputBlock.block : inputBlock.shadow);

    return `${variableName} += ${input}`;
}

function textLengthHandler(block) {
    if (block === undefined) return '';
    const aSlot = block.inputs.VALUE;
    const a = parseBlock(aSlot.block === undefined ? aSlot.shadow : aSlot.block);
    return `len(${a})`;
}

function textIndexOfHandler(block) {
    if (block === undefined) return '';

    const valueSlot = block.inputs.VALUE;
    const findSlot = block.inputs.FIND;

    const value = valueSlot ? parseBlock(valueSlot.block) : '[value]';
    const find = parseBlock(findSlot.block ? findSlot.block : findSlot.shadow);

    switch (block.fields.END) {
        case 'FIRST':
            return `${value}.find(${find})`;
        case 'LAST':
            return `${value}.rfind(${find})`;
    }

    return '';
}

function textCharAtHandler(block) {
    if (block === undefined) return '';

    const valueSlot = block.inputs.VALUE;
    const value = valueSlot ? parseBlock(valueSlot.block) : '[value]';

    if (block.fields.WHERE === 'FROM_START' || block.fields.WHERE === 'FROM_END') {
        const atSlot = block.inputs.AT;
        const at = atSlot ? parseBlock(atSlot.block) : '[at]';
        switch(block.fields.WHERE) {
            case 'FROM_START':
                return `${value}[${at - 1}]`;
            case 'FROM_END':
                return `${value}[${at * -1}]`;
        }
    }

    switch(block.fields.WHERE) {
        case 'FIRST':
            return `${value}[0]`;
        case 'LAST':
            return `${value}[-1]`;
        case 'RANDOM':
            return `${value}[random.randint(0, len(${value}))]`;
    }

    return '';
}

function textGetSubStringHandler(block) {
    if (block === undefined) return '';

    const stringSlot = block.inputs ? block.inputs.STRING : undefined;
    const string = stringSlot ? parseBlock(stringSlot.block) : '[string]';

    const at1Slot = block.inputs ? block.inputs.AT1 : undefined;
    const at1 = at1Slot ? parseBlock(at1Slot.block) : '[at1]';

    const at2Slot = block.inputs ? block.inputs.AT2 : undefined;
    const at2 = at2Slot ? parseBlock(at2Slot.block) : '[at2]';

    let listOpNum1 = '';
    if (at1Slot) {
        switch(block.fields.WHERE1) {
            case 'FROM_START':
                listOpNum1 = at1 - 1;
            case 'FIRST':
                break;
            case 'FROM_END':
                listOpNum1 = at1 * -1;
        }
    }

    let listOpNum2 = '';
    if (at2Slot) {
        switch(block.fields.WHERE2) {
            case 'FROM_START':
                listOpNum2 = at2 - 1;
            case 'L':
                break;
            case 'FROM_END':
                listOpNum2 = at2 * -1;
        }
    }

    return `${string}[${listOpNum1}:${listOpNum2}]`;
}

function textChangeCaseHandler(block) {
    if (block === undefined) return '';

    const textSlot = block.inputs.TEXT;
    const text = textSlot.shadow ? parseBlock(textSlot.shadow) : parseBlock(testSlot.block);

    switch(block.fields.CASE) {
        case 'UPPERCASE':
            return `${text}.upper()`;
        case 'LOWERCASE':
            return `${text}.lower()`;
        case 'TITLECASE':
            return `${text}.title()`;
    }

    return '';
}

function textCountHandler(block) {
    if (block === undefined) return '';

    const subSlot = block.inputs.SUB;
    const sub = subSlot.shadow ? parseBlock(subSlot.shadow) : parseBlock(subSlot.block);

    const textSlot = block.inputs.TEXT;
    const text = textSlot.shadow ? parseBlock(textSlot.shadow) : parseBlock(textSlot.block);

    return `${text}.count(${sub})`;
}

function textReverseHandler(block) {
    if (block === undefined) return '';

    const textSlot = block.inputs.TEXT;
    const text = textSlot.shadow ? parseBlock(textSlot.shadow) : parseBlock(textSlot.block);

    return `${text}[::-1]`;
}

function textPrintHandler(block) {
    if (block === undefined) return '';

    const textSlot = block.inputs.TEXT;
    const text = textSlot.shadow ? parseBlock(textSlot.shadow) : parseBlock(textSlot.block);

    return `print(${text})\n`;
}

function textPromptExtHandler(block) {
    if (block === undefined) return '';

    const textSlot = block.inputs.TEXT;
    const text = textSlot.shadow ? parseBlock(textSlot.shadow) : parseBlock(textSlot.block);

    switch(block.fields.TYPE) {
        case 'TEXT':
            return `input(${text})`;
        case 'NUMBER':
            return `int(input(${text}))`;
    }
    
    return '';
}
 
//VARIABLES

const SCRIPT_VARIABLES = {};

function variablesSetHandler(block) {
    if (block === undefined) return '';
    const variableName = SCRIPT_VARIABLES[block.fields.VAR.id];
    const expression = block.inputs === undefined ? '' : parseBlock(block.inputs.VALUE.block);
    return `${variableName} = ${expression}\n`; 
}

function mathChangeHandler(block) {
    if (block === undefined) return '';
    const variableName = SCRIPT_VARIABLES[block.fields.VAR.id];
    const input = block.inputs.DELTA;
    const delta = input.block === undefined ? parseBlock(input.shadow) : parseBlock(input.block);
    return `${variableName} += ${delta}`;
}

function variablesGetHandler(block) {
    if (block === undefined) return '';
    return SCRIPT_VARIABLES[block.fields.VAR.id];
}

//PARSER

function createNestedComponent(block) {
    let code = '';
    let curBlock = block;
    while (curBlock !== undefined) {
        const processedBlock = parseBlock(curBlock);
        const lines = processedBlock.split('\n');
        lines.forEach(line => code += `\t${line}\n`);
        curBlock = curBlock.next === undefined ? undefined : curBlock.next.block;          
    }
    return code;
}

function parseBlock(block) {
    if (block === undefined) return '';
    console.log(block);
    switch (block.type) {
        case 'controls_if':
            return controlIfHandler(block);
        case 'controls_whileUntil':
            return controlWhileUntilHandler(block);
        case 'controls_for':
            return controlForHandler(block);
        case 'controls_forEach':
            return controlForEachHandler(block);
        case 'controls_flow_statements':
            return controlFlowStatementHandler(block);
        case 'math_number':
            return block.fields.NUM;
        case 'math_arithmetic':
            return mathArithmeticHandler(block);
        case 'math_single':
            return mathSingleHandler(block);
        case 'math_trig':
            return mathTrigHandler(block);
        case 'math_constant':
            return mathConstantHandler(block);
        case 'math_on_list':
            return mathOnListHandler(block);
        case 'math_modulo':
            return mathModuloHandler(block);
        case 'math_random_int':
            return mathRandomIntHandler(block);
        case 'math_atan2':
            return mathATan2Handler(block);
        case 'text':
            return textHandler(block);
        case 'text_append':
            return textAppendHandler(block);
        case 'text_length':
            return textLengthHandler(block);
        case 'text_indexOf':
            return textIndexOfHandler(block);
        case 'text_charAt':
            return textCharAtHandler(block);
        case 'text_getSubstring':
            return textGetSubStringHandler(block);
        case 'text_changeCase':
            return textChangeCaseHandler(block);
        case 'text_count':
            return textCountHandler(block);
        case 'text_reverse':
            return textReverseHandler(block);
        case 'text_print':
            return textPrintHandler(block);
        case 'text_prompt_ext':
            return textPromptExtHandler(block);
        case 'variables_set':
            return variablesSetHandler(block);
        case 'math_change': 
            return mathChangeHandler(block);
        case 'variables_get':
            return variablesGetHandler(block);
        default:
            return '';
    }
}

function btop(code) {
    if (code === '') return '';
    if (code.blocks === undefined) return '';
    if (code.variables !== undefined) 
        code.variables.forEach(variable => SCRIPT_VARIABLES[variable.id] = variable.name);
    let pythonCode = '';
    let curBlock = code.blocks.blocks[0];
    while (curBlock !== undefined) {
        pythonCode += parseBlock(curBlock);
        curBlock = curBlock.next === undefined ? undefined : curBlock.next.block;
    }
    return pythonCode;
}

export { btop };
