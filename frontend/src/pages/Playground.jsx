import { React, Suspense, lazy, useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Markdown from 'react-markdown';
import { tryGetModule } from '$lib/utils/actions.mjs';
import { AuthUserContext, ErrorContext } from '$lib/contexts/Context';

const CodeEditor = lazy(() => import('$lib/components/CodeEditor'));

export default function Playground() {
  const { module_id } = useParams();
  const [module, setModule] = useState(null);
  const { setError } = useContext(ErrorContext);
  const { authUser } = useContext(AuthUserContext)
  useEffect(() => {
    if (module_id){
    tryGetModule(authUser, module_id).then((res) => {
      if (res instanceof Error) return setError(res.message)
      else setModule(res)
    })}

  }, [setError, setModule, module_id, authUser]);
  return (
    <main className="grid flex-1 grid-cols-2">
      <Suspense
        fallback={
          <main className={`col-span-2 flex-1 justify-self-center`}>
            code editor loading...
          </main>
        }
      >
        <CodeEditor
          className={`flex h-full flex-col ${!module_id ? 'col-span-2' : ''}`}
        />
        <aside
          className={`m-1 flex flex-col rounded bg-zinc-800 ${!module_id ? 'hidden' : ''}`}
        >
          <h1 className="p-2 text-2xl"> {module ? module.module_name : ''}</h1>
          <aside
            className={`m-2 h-full flex-1 rounded bg-zinc-900 p-2 ${!module_id ? 'hidden' : ''}`}
          >
            <Markdown>
              {module ? module.blob : ''}
            </Markdown>
          </aside>
        </aside>
      </Suspense>
    </main>
  );
}
