import { React, Suspense, lazy } from 'react';

const CodeEditor = lazy(() => import("$lib/components/CodeEditor"));

export default function Playground() {
    // TODO - add console
    return (
        <div className="w-full h-blockly"> 
            <Suspense fallback={<div>code editor loading...</div>} >
                <CodeEditor />
            </Suspense>
        </div>
    );
}
