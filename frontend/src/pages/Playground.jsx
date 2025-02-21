import { React, Suspense, lazy } from 'react';

const CodeEditor = lazy(() => import("../components/CodeEditor"));

export default function Playground() {
    // TODO - add console
    return (
        <div className="w-full h-full"> 
            <Suspense fallback={<div>code editor loading...</div>} >
                <CodeEditor />
            </Suspense>
        </div>
    );
}
