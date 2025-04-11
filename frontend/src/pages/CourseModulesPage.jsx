import CourseModulesWidget from "$lib/components/CourseModulesWidget";
import { useParams } from "react-router-dom";

export default function CourseModulesPage() {
  const { courseid } = useParams();

  return (
    <main className="flex flex-1 flex-col items-center justify-start md:my-10">
      <CourseModulesWidget className="m-2 w-full max-w-4xl rounded bg-zinc-800 p-4" courseId={courseid} />
    </main>
  );
}
