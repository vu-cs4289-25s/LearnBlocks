import GoToPlaygroundModal from '$lib/components/GoToPlaygroundModal';
import UpcomingLessonWidget from '$lib/components/UpcomingLessonWidget';
import ClassesWidget from '$lib/components/ClassesWidget';

export default function TeacherHomePage() {
  return (
    <main className="m-2 flex flex-1 flex-col gap-4 md:flex-row md:my-10 md:gap-6 md:items-stretch">
      {/* Left column */}
      <section className="flex flex-col gap-4 flex-1 md:max-w-2xl">
        <UpcomingLessonWidget className="flex flex-col rounded bg-zinc-800 p-2" />
        <GoToPlaygroundModal className="grid min-h-0 w-full flex-1 basis-0 grid-cols-2 rounded bg-zinc-800" />
      </section>

      {/* Right column */}
      <section className="flex flex-col gap-4 flex-1 md:max-w-2xl">
        <ClassesWidget className="flex flex-col rounded bg-zinc-800 p-2" />
      </section>
    </main>
  );
}
