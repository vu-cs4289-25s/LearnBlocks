import { AuthUserContext, ErrorContext } from '$lib/contexts/Context';
import { tryGetCourse } from '$lib/utils/actions.mjs';
import { skeleton_course } from '$lib/utils/skeleton.mjs';
import { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function CourseModulesWidget({ className, courseId }) {
  const [course, setCourse] = useState(skeleton_course);
  const { setError } = useContext(ErrorContext);
  const { authUser } = useContext(AuthUserContext);

  useEffect(() => {
    tryGetCourse(authUser, courseId)
      .then((course) => setCourse(course))
      .catch((err) => setError(err));
  }, [authUser, courseId, setError]);

  return (
    <section className={className}>
      <h1 className="mb-4 text-2xl font-bold text-white">
        Modules for Course {course.course_name}
      </h1>

      <ul className="flex flex-col gap-2">
        {course.modules.map((mod, key) => (
          <li
            key={key}
            className="flex flex-col items-start justify-between gap-2 rounded bg-zinc-900 p-4 text-zinc-300 transition hover:bg-zinc-800 md:flex-row md:items-center"
          >
            <div>
              <h2 className="text-lg font-semibold text-white">
                {mod.module_name}
              </h2>
            </div>

            <div className="flex items-center gap-2 self-end md:self-auto">
              <Link
                to={`/catalog/${courseId}/module/${mod.id}`}
                className="rounded border border-amber-400 px-3 py-1 text-xs font-medium hover:bg-amber-400 hover:text-black active:bg-amber-500"
              >
                Enter
              </Link>
            </div>
          </li>
        ))}
      </ul>

      <div className="mt-6 flex justify-center">
        <Link
          to="/catalog"
          className="transition-color w-40 rounded-full border border-amber-400 px-3 py-1 text-center text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
        >
          Back to Catalog
        </Link>
      </div>
    </section>
  );
}
