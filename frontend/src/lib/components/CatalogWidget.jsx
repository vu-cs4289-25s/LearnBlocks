import { useState } from 'react';
import { Link } from 'react-router-dom';
import PageSelector from './PageSelector';

/**
 * @param {object} props
 * @param {string} props.className
 */
export default function CatalogWidget({ className }) {
  const data = [];
  const itemsPerPage = 4;

  for (let i = 0; i < 12; i++) {
    if (i % itemsPerPage === 0) data.push([]);
    data.at(-1).push({
      name: `Course ${i + 1}`,
      description: `This is a brief description for Course ${i + 1}.`,
    });
  }

  const [page, setPage] = useState(1);

  return (
    <section className={className}>
      <h1 className="mb-4 text-3xl font-bold text-white">Course Catalog</h1>
      <ul className="flex flex-col gap-4 overflow-auto rounded border-6 border-zinc-900 bg-zinc-900 p-4">
        {data[page - 1].map((course, key) => {
          const courseId = (page - 1) * itemsPerPage + key;
          return (
            <li
              key={courseId}
              className="flex flex-col gap-2 rounded bg-zinc-800 p-5 text-zinc-300 shadow hover:bg-zinc-700 transition"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-white">{course.name}</h2>
                  <p className="text-sm text-zinc-400">{course.description}</p>
                </div>
                <Link
                  to={`/catalog/${courseId}`}
                  className="self-center rounded bg-amber-400 px-4 py-2 text-sm font-medium text-black hover:bg-amber-500"
                >
                  View Modules
                </Link>
              </div>
            </li>
          );
        })}
      </ul>

      <div className="mt-4 flex flex-col gap-3">
        {/* Pagination aligned right */}
        <div className="flex justify-end">
          <PageSelector page={page} setPage={setPage} arr={data} />
        </div>

        {/* Centered Button */}
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
