import { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import PageSelector from './PageSelector';
import { tryGetCatalog } from '$lib/utils/actions.mjs';
import { AuthUserContext, ErrorContext } from '$lib/contexts/Context';
import courses from '$lib/courses';
import { skeleton_course } from '$lib/utils/skeleton.mjs';

/**
 * @param {object} props
 * @param {string} props.className
 */
export default function CatalogWidget({ className }) {
  const itemsPerPage = 4;

  const [catalog, setCatalog] = useState([[skeleton_course]]);
  const { authUser } = useContext(AuthUserContext);
  const { setError } = useContext(ErrorContext);

  useEffect(() => {
    tryGetCatalog(authUser)
      .then((res) => {
        const newCatalog = [];
        for (let i = 0; i < res.length; i += 1) {
          if (i % itemsPerPage === 0) newCatalog.push([]);
          newCatalog.at(-1).push(res[i]);
        }
        setCatalog(newCatalog);
      })
      .catch((err) => setError(err));
  }, [authUser, setError]);

  const [page, setPage] = useState(1);

  return (
    <section className={className}>
      <h1 className="mb-4 text-3xl font-bold text-white">Course Catalog</h1>

      <ul className="flex flex-col gap-4 overflow-auto rounded border-6 border-zinc-900 bg-zinc-900 p-4">
        {catalog[page - 1].map((course, key) => {
          return (
            <li
              key={key}
              className="flex flex-col gap-2 rounded bg-zinc-800 p-5 text-zinc-300 shadow transition hover:bg-zinc-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-white">
                    {course.course_name}
                  </h2>
                  <p>
                    <h2 className="font-semibold">Modules: </h2>
                    {course.modules.map((module, key) => (
                      <text key={key}>{module.module_name + ' / '}</text>
                    ))}
                  </p>
                </div>
                <Link
                  to={`/catalog/${course.course_id}`}
                  className="self-center rounded px-4 py-2 text-sm font-medium outline outline-amber-400 hover:bg-amber-400 hover:text-black active:bg-amber-500"
                >
                  View Modules
                </Link>
              </div>
            </li>
          );
        })}
      </ul>
      <div className="mt-4 flex flex-col gap-3">
        <div className="flex justify-center">
          <PageSelector page={page} setPage={setPage} arr={catalog} />
        </div>

        <div className="flex justify-center">
          <Link
            to="/"
            className="transition-color rounded-full border border-amber-400 px-4 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </section>
  );
}
