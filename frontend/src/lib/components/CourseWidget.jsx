import { Link } from 'react-router-dom';

/**
 *
 * @param props
 * @param props.course
 * @returns {import("react").ReactElement}
 */
export default function CourseWidget({ course, className }) {
  return (
    <section className={className} >
      <h2 className="font-semibold text-zinc-100">{course.name}</h2>
      <hr className="text-zinc-700" />
      <ul className="flex flex-1 snap-x snap-mandatory flex-row items-center gap-8 overflow-auto rounded border-zinc-900 bg-zinc-900 ">
        {course.modules.map((project, key) => {
          const color =
            project.status === 'Complete'
              ? 'active:bg-yellow-600 hover:bg-yellow-500 border-yellow-500'
              : project.status === 'Locked'
                ? 'border-zinc-700'
                : 'active:bg-amber-800 hover:bg-amber-700 border-amber-700';
          return (
            <li
              className="flex min-h-1/2 min-w-1/2 snap-center flex-col items-center justify-evenly rounded bg-zinc-800 p-2 text-center align-middle text-sm font-semibold text-zinc-100"
              key={key}
            >
              {project.name}
              <p className="text-xs font-light text-zinc-400">
                This module does this and this and this
              </p>
              <Link
                to={project.link}
                className={`min-w-4/6 rounded-full border ${color} }`}
              >
                {project.status}
              </Link>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
