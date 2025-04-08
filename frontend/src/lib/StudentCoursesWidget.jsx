import { Button } from "@headlessui/react";
import { Link } from "react-router-dom";
import CourseWidget from "./components/CourseWidget";
import { useContext, useEffect, useState } from "react";
import PageSelector from "./components/PageSelector";
import { tryGetCourses } from "./utils/actions.mjs";
import { ErrorContext } from "./contexts/ErrorContext";
import { chunkArray } from "./utils/misc.mjs";

const example = {
  name: "example",
  modules: [
    { name: "module 1", status: "Complete", link: "/playground" },
    { name: "module 2", status: "Complete", link: "/playground" },
    { name: "module 3", status: "In Progress", link: "/playground" },
    { name: "module 4", status: "Locked", link: "" },
    { name: "module 5", status: "Locked", link: "" },
  ],
};

export default function StudentCoursesWidget({ className }) {
  const [page, setPage] = useState(1);
  const [courses, setCourses] = useState([[]]);
  const { setError } = useContext(ErrorContext);

  useEffect(() => {
    tryGetCourses().then((res) => {
      if (res instanceof Error) {
        setError(res.message);
        return
      }
      setCourses(chunkArray(res, 3))
    });
  }, [setError]);

  return (
    <section className={className}>
      <h1 className="text-xl font-bold">My Courses </h1>
      <hr className="text-center text-zinc-700" />
      <ul className="flex-1 grid grid-rows-3 gap-2">
        {courses[page - 1].map((example, key) => {
          return (
            <CourseWidget
              course={example}
              key={key}
              className={
                "rounded border-10 border-zinc-900 bg-zinc-900 flex flex-col min-w-xs"
              }
            />
          );
        })}
      </ul>
      <PageSelector page={page} setPage={setPage} arr={courses} />
    </section>
  );
}
