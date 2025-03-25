import { pythonGenerator } from 'blockly/python';

function btop(workspace) {
    return pythonGenerator.workspaceToCode(workspace);
}

export { btop };
