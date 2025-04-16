import StudentCoursesWidget from "$lib/StudentCoursesWidget";

export default function StudentCoursesPage() {
  return (
    <main className="flex max-w-md flex-1 flex-col items-center justify-evenly gap-2 self-center p-2 md:my-20 md:max-w-xl md:flex-row md:items-stretch md:gap-4">
        <StudentCoursesWidget className="flex flex-1 flex-col rounded bg-zinc-800 p-2 md:order-3 gap-2" />
    </main>
  );
}
