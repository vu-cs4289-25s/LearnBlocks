import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Button } from "@headlessui/react";
import { BlocklyWorkspace } from 'react-blockly';
import * as Blockly from 'blockly/core';
import { btop, ptob } from '$lib/utils/transpile.js';
import { TOOLBOX } from '$lib/utils/blocklyToolbox.js';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

// TODO - create theme
const WORKSPACE_CONFIG = {
    theme: {
        'componentStyles' : {
            'workspaceBackgroundColour': '#1D1D1D',
            'toolboxBackgroundColour': '#2B2B2B',
            'flyoutBackgroundColour': '#1D1D1D',
            'flyoutOpacity': 1,
            'scrollbarColour': '#797979',
            'insertionMarkerColour': '#fff',
        },
        'blockStyles' : {
            'logic_blocks' : {
                'colourPrimary': '#e5a823'
            },
            'math_blocks' : {
                'colourPrimary': '#62c20f'
            },
            'text_blocks' : {
                'colourPrimary': '#8e57e4'
            },
            'loop_blocks' : {
                'colourPrimary': '#4c6cd4'
            },
            'list_blocks' : {
                'colourPrimary': '#d94d12'
            },
            'variable_blocks' : {
                'colourPrimary': '#f4761c'
            },
            'procedure_blocks' : {
                'colourPrimary': '#d94d12'
            }
        },
        'categoryStyles': {
            'logic_category': {
                'colour': '#e5a823'
            },
            'math_category': {
                'colour': '#62c20f'
            },
            'text_category': {
                'colour': '#8e57e4'
            },
            'loop_category': {
                'colour': '#4c6cd4'
            },
            'list_category': {
                'colour': '#d94d12'
            },
            'variable_category': {
                'colour': '#f4761c'
            },
            'procedure_category': {
                'colour': '#d94d12'
            }
        }
    }
};

const BlocklyComponent = ({ globalState, setLocalState }) => {
    return (
        <BlocklyWorkspace 
          className='w-full h-full border-2 border-gray-700'
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
          className='resize-none w-full h-full border-2 border-black bg-gray-800'
          onInput={saveState}
        />
    );
}

export default function CodeEditor() {
    const [editorMode, setEditorMode] = useState('blockly');
    const [globalState, setGlobalState] = useState('');
    const [pythonLocalState, setPythonLocalState] = useState('');
    const [consoleState, setConsoleState] = useState('$');

    const changeLanguage = () => {
        if (editorMode === 'blockly') {
            setEditorMode('python');
        } else {
            setEditorMode('blockly');
        }
        resetConsole();
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

    const runCode = () => {
        setConsoleState('running...');
        // TODO
    }

    const resetConsole = () => {
        setConsoleState('$');
    }

    const saveCode = () => {
        resetConsole()
        console.log(globalState)
        //TODO
    }

    return (
        <div className='w-full h-full inline-flex'>
          <div className='w-3/5 h-full'>
              {
                editorMode === 'blockly' ?
                <BlocklyComponent globalState={globalState} setLocalState={updateBlocklyState} /> :
                <PythonEditor globalState={globalState} setLocalState={updatePythonState} />
              }
            <div className='flex space-x-3 py-2 px-1'>
              <Button
                className="rounded-full border border-amber-500 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:shadow text-amber-500"
                onClick={changeLanguage}
              >
                {editorMode === 'blockly' ? 'switch to python' : 'switch to blockly'}
              </Button>
              <Button
                className="rounded-full border border-green-400 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:shadow text-green-400"
                onClick={runCode}
              >
                Run Code
              </Button>
              <Button
                className="rounded-full border border-yellow-200 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:shadow text-yellow-200"
                onClick={saveCode}
               >
                 Save
               </Button>
            </div>
          </div>
          <div className="w-1/5 h-full">
              {consoleState}
          </div>
        </div>
    );
}
