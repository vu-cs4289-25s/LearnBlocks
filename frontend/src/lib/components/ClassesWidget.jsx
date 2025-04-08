import { useState } from 'react';
import PageSelector from './PageSelector';
import { Link } from 'react-router-dom';

/**
 *
 * @param {object} props - the props for this component
 * @param {string} props.className - passed directly to the first element of this component
 * @returns {import("react").ReactElement} a paged list of the public courses.
 */
export default function ClassesWidget({ className }) {
  const data = [];
  for (let i = 0; i < 10; i++) {
    if (i % 6 === 0) data.push([]);
    data.at(-1).push({
      course_id: i,
      name: 'Class ' + i,
      description: 'Description ' + i,
    });
  }

  const [page, setPage] = useState(1);

  return (
    <main className={className}>
      <h1 className="text-xl font-bold text-white mb-2">Classes</h1>
      <hr className="text-zinc-400 mb-2" />

      <ul className="flex flex-col gap-2 flex-1">
        {data[page - 1].map((course, key) => (
          <li className="rounded bg-zinc-900 p-2" key={key}>
            <div className="mb-2 flex items-center justify-between">
              <h1 className="text-md font-semibold">{course.name}</h1>
              <Link
                to={`/t/classes/${course.course_id}/students`}
                className="inline-block rounded bg-amber-400 px-2 py-0.5 text-xs text-black hover:bg-amber-500"
              >
                View Students
              </Link>
            </div>
            <hr className="h-0.5 text-zinc-800" />
            <p className="text-xs">{course.description}</p>
          </li>
        ))}
      </ul>
      <PageSelector page={page} setPage={setPage} arr={data} />
    </main>
  );
}
