import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BlocklyWorkspace } from 'react-blockly';
import { Button, Dropdown } from 'flowbite-react';
import { btop } from '$lib/utils/transpile.js';
import { TOOLBOX } from '$lib/utils/blocklyToolbox.js';

// TODO - create theme
const WORKSPACE_CONFIG = {
    theme: {
        'componentStyles' : {
            'workspaceBackgroundColour' : '#272823'
        }
    }
};

const BlocklyComponent = props => {
    return (
        <BlocklyWorkspace 
          className='w-2/3 h-96'
          toolboxConfiguration={TOOLBOX}
          workspaceConfiguration={WORKSPACE_CONFIG}
          initialJson={null}
          onJsonChange={props.setState}
        />
    );
};

const PythonEditor = props => {
    const [state, setState] = useState('');
    
    const saveState = event => {
        setState(event.target.value);
    }

    useEffect(() => {
        const pythonCode = btop(props.state);
        setState(pythonCode);
    }, []);  

    return (
        <textarea 
          value={state}
          className='resize-none w-2/3 h-96' 
          onInput={saveState}
        />
    );
}

export default function CodeEditor() {
    const [editorMode, setEditorMode] = useState('blockly');
    const [editorState, setEditorState] = useState('');

    const changeLanguage = () => {
        if (editorMode === 'blockly') {
            setEditorMode('python');
        } else {
            setEditorMode('blockly');
        }
    } 

    return (
        <div className='w-full h-full'>
            {
              editorMode === 'blockly' ? 
              <BlocklyComponent setState={setEditorState} /> : 
              <PythonEditor state={editorState} />
            }
            <div className='flex space-x-3'>
                <Button color='dark' size='sm' onClick={changeLanguage}>
                    {editorMode === 'blockly' ? 'switch to python' : 'switch to blockly'}
                </Button>
                <Button color='dark' size='sm'>Run Code</Button>
            </div>
        </div>
    );
}
