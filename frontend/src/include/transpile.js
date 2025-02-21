//LOGIC

function createLogicCompare(block) {
    if (block.fields.OP === 'EQ') {
        const a = parseBlock(block.inputs.A.block);
        const b = parseBlock(block.inputs.B.block);
        return `${a} = ${b}`;
    };
    return '';
 }

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
    console.log(variableName);
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
        case 'math_number':
            return block.fields.NUM;
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
