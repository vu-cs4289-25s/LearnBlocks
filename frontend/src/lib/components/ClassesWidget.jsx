import { Link } from 'react-router-dom';

/**
 * @param {object} props
 * @param {string} props.className
 */
export default function ClassesWidget({ className }) {
  const data = Array.from({ length: 20 }, (_, i) => ({
    course_id: i,
    name: `Class ${i}`,
    description: `Description ${i}`,
  }));

  return (
    <section className={className}>
      <h1 className="text-xl font-bold text-white mb-2">Classes</h1>
      <hr className="text-zinc-400 mb-2" />
      <ul className="flex flex-col gap-2 overflow-auto rounded border-6 border-zinc-900 bg-zinc-900 p-2">
        {data.map((course, key) => (
          <li
            className="flex flex-col gap-1 rounded bg-zinc-800 p-2 text-zinc-300"
            key={key}
          >
            <div className="flex items-center justify-between">
              <h2 className="font-semibold">{course.name}</h2>
              <Link
                to={`/t/classes/${course.course_id}/students`}
                className="self-center rounded bg-amber-400 px-3 py-1 text-xs font-medium text-black hover:bg-amber-500"
              >
                View Students
              </Link>
            </div>
            <p className="text-xs text-zinc-400">{course.description}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
