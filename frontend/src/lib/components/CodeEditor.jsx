import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { BlocklyWorkspace } from 'react-blockly';
import * as Blockly from 'blockly/core';
import { btop, ptob } from '$lib/utils/transpile.js';
import { TOOLBOX } from '$lib/utils/blocklyToolbox.js';

// TODO - create theme
const WORKSPACE_CONFIG = {
    theme: {
        'componentStyles' : {
            'workspaceBackgroundColour' : '#272823'
        }
    }
};

const BlocklyComponent = ({ globalState, setLocalState }) => {
    return (
        <BlocklyWorkspace 
          className='w-2/3 h-96'
          toolboxConfiguration={TOOLBOX}
          workspaceConfiguration={WORKSPACE_CONFIG}
          initialJson={ptob(globalState)}
          onWorkspaceChange={setLocalState}
        />
    );
};

const PythonEditor = ({ globalState, setLocalState }) => {
    const [state, setState] = useState('');
    
    const saveState = event => {
        setState(event.target.value);
        setLocalState(event.target.value);
    }

    useEffect(() => {
        setState(globalState);
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
    const [globalState, setGlobalState] = useState('');
    const [pythonLocalState, setPythonLocalState] = useState('');

    const changeLanguage = () => {
        if (editorMode === 'blockly') {
            setEditorMode('python');
        } else {
            setEditorMode('blockly');
        }
    }

    const updateBlocklyState = workspace => {
        console.log(Blockly.serialization.workspaces.save(workspace));
        const transpiledCode = btop(workspace);
        setGlobalState(transpiledCode);
    }

    const updatePythonState = pythonSource => {
        const parsedSource = ptob(pythonSource);
       
        if (!parsedSource['error'])
            setGlobalState(pythonSource);
        else
            console.log(parsedSource);
    }

    return (
        <div className='w-full h-full'>
            {
              editorMode === 'blockly' ? 
              <BlocklyComponent globalState={globalState} setLocalState={updateBlocklyState} /> : 
              <PythonEditor globalState={globalState} setLocalState={updatePythonState} />
            }
            <div className='flex space-x-3'>
                <button color='dark' size='sm' onClick={changeLanguage}>
                    {editorMode === 'blockly' ? 'switch to python' : 'switch to blockly'}
                </button>
                <button color='dark' size='sm'>Run Code</button>
            </div>
        </div>
    );
}
