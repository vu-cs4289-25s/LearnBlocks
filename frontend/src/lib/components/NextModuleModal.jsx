import { Link } from "react-router-dom";
import CourseWidget from "./CourseWidget";
import { useContext, useEffect, useState } from "react";
import { tryListCourses } from "$lib/utils/actions.mjs";
import { AuthUserContext, ErrorContext } from "$lib/contexts/Context";

export default function RecentCourseModal({ className }) {
  const [course, setCourse] = useState(null);
  const { setError } = useContext(ErrorContext);
  const { authUser } = useContext(AuthUserContext);
  useEffect(() => {
    tryListCourses(authUser).then((res) => {
      if (res instanceof Error) {
        return setError(res.message);
      }
      setCourse(res[0]);
    });
  }, [setError]);

  return (
    <section className={className}>
      <h1 className="text-xl font-bold">Recent Course</h1>
      <hr className="mb-2 text-center text-zinc-700" />
      {course ? (
        <CourseWidget
          course={course}
          className="flex flex-1 flex-col rounded border-10 border-zinc-900 bg-zinc-900"
        />
      ) : null}
      <section className="col-span-2 flex flex-col items-center justify-center gap-4">
        <Link 
          to="/catalog"
          className="transition-color w-1/2 rounded-full border-2 border-amber-700 text-center shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800">
          Browse Catalog
        </Link>
      </section>
    </section>
  );
}
