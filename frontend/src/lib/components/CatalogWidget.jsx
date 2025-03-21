import { Button } from '@headlessui/react';
import { useState } from 'react';
import PageSelector from './PageSelector';

/**
 *
 * @param {object} props - the props for this component
 * @param {string} props.className - passed directly to the first element of this component
 * @returns {import("react").ReactElement} a paged list of the public courses.
 */
export default function CatalogWidget({ className }) {
  const data = [];
  for (let i = 0; i < 10; i++) {
    if (i % 6 === 0) data.push(new Array());
    data.at(-1).push({
      course_id: i,
      name: 'Course ' + i,
      description: 'Description ' + i,
    });
  }

  const [page, setPage] = useState(1);

  return (
    <main className={className}>
      <ul className="flex-1">
        {data[page - 1].map((course, key) => (
          <li className="m-2 h-1/7 rounded bg-zinc-900 p-2" key={key}>
            <h1>{course.name}</h1>
            <hr className="h-0.5 text-zinc-800" />
            <p className="text-xs">{course.description}</p>
          </li>
        ))}
      </ul>

      <PageSelector page={page} setPage={setPage} arr={data} />
    </main>
  );
}
