import { pythonGenerator } from 'blockly/python';
import init, { ptob_wasm } from '$lib/blockly-transpiler/pkg/blockly_transpiler'

await init();

function btop(workspace) {
    return pythonGenerator.workspaceToCode(workspace);
}

function ptob(pythonSource) {
    if (pythonSource === '')
        return { 'error': 'empty python'}
    const transpiledCode = ptob_wasm(pythonSource);
    try {
        const validJson = JSON.parse(transpiledCode);
        if (validJson['error']) {
            return { 
                'error': 'could not parse python code',
                'details': transpiledCode,
            }
        }
        return validJson;
    } catch (SyntaxError) {
        return { 
            'error': 'invalid jason returned from the parser',
            'details': transpiledCode,
        }
    }
}

export { btop, ptob };
