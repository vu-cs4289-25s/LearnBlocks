import  { useState, useEffect } from 'react';
import { Button } from "@headlessui/react";
import * as Blockly from 'blockly/core';
import { javascriptGenerator } from 'blockly/javascript';
import { btop, ptob } from '$lib/utils/transpile.js';
import { TOOLBOX } from '$lib/utils/blocklyToolbox.js';
import { BlocklyWorkspace } from 'react-blockly';

const WORKSPACE_CONFIG = {
    theme: {
        'componentStyles' : {
            'workspaceBackgroundColour': '#1D1D1D',
            'toolboxBackgroundColour': '#2B2B2B',
            'flyoutBackgroundColour': '#18181b',
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

const BlocklyComponent = ({ globalState, setGlobalState }) => {
    return (
        <BlocklyWorkspace 
          className='w-full h-full border-2 border-gray-700'
          toolboxConfiguration={TOOLBOX}
          workspaceConfiguration={WORKSPACE_CONFIG}
          initialJson={globalState}
          onWorkspaceChange={setGlobalState}
        />
    );
};

const PythonEditor = ({ pythonLocalState, setLocalState }) => {
    const [state, setState] = useState('');
    
    const saveState = event => {
        setState(event.target.value);
        setLocalState(event.target.value);
    }

    useEffect(() => {
        setState(pythonLocalState);
    }, []);  

    return (
        <textarea 
          value={state}
          className='resize-none w-full h-full border-2 border-zinc-600 bg-slate-800 '
          onInput={saveState}
        />
    );
}

export default function CodeEditor({className}) {

    const [editorMode, setEditorMode] = useState('blockly');
    const [globalState, setGlobalState] = useState({});
    const [pythonLocalState, setPythonLocalState] = useState('');
    const [workspace, setWorkspace] = useState(undefined);

    const changeLanguage = () => {
        if (editorMode === 'blockly') {
            setEditorMode('python');
        } else {
            setEditorMode('blockly');
        }
    }

    const updateBlocklyState = _workspace => {
        setWorkspace(_workspace);
        if (workspace) {
            const serialized_state = Blockly.serialization.workspaces.save(workspace);
            if (JSON.stringify(serialized_state) !== JSON.stringify(globalState)) {
                setGlobalState(serialized_state);
                setPythonLocalState(btop(workspace));
            }
        }
    }

    const updatePythonState = pythonSource => {
        const parsedSource = ptob(pythonSource);
        if (!parsedSource['error'])
            setGlobalState(parsedSource);
        else
            console.log(parsedSource);
    }

    const runCode = () => {
        javascriptGenerator.addReservedWords('code');
        javascriptGenerator.addReservedWords
        var code = javascriptGenerator.workspaceToCode(workspace);
        try {
            eval(code);
        } catch (e) {
            alert(e);
        }
    }

    const saveCode = () => {
        console.log(globalState)
        //TODO
    }

    return (
        <div className={className}>
          <div className='flex space-x-3 py-2 px-1 border-zinc-700 bg-zinc-800 mt-1 rounded-t'>
            <Button
              className="rounded-full bg-zinc-900 border-2 border-amber-700 px-2 py-1 text-amber-600 font-semibold hover:bg-amber-700 active:bg-amber-800 hover:text-white"
              onClick={changeLanguage}
            >
              {editorMode === 'blockly' ? 'switch to python' : 'switch to blockly'}
            </Button>
            <Button
              className="rounded-full bg-zinc-900 border-2 border-green-600 px-2 py-1 text-green-600 font-semibold hover:bg-green-700 active:bg-green-800 hover:text-white"
              onClick={runCode}
            >
              Run Code
            </Button>
            <Button
              className="rounded-full bg-zinc-900 border-2 border-zinc-600 px-2 py-1 text-zinc-600 font-semibold disabled cursor-not-allowed"
              onClick={saveCode}
             >
               Save
             </Button>
          </div>
          <div className='w-full h-full'>
              {
                editorMode === 'blockly' ?
                <BlocklyComponent globalState={globalState} setGlobalState={updateBlocklyState} /> :
                <PythonEditor 
                  pythonLocalState={pythonLocalState}
                  setLocalState={updatePythonState} 
                />
              }
          </div>
        </div>
    );
}
