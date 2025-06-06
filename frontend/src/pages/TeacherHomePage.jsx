import GoToPlaygroundModal from '$lib/components/GoToPlaygroundModal';
import ClassesWidget from '$lib/components/ClassesWidget';

export default function TeacherHomePage() {
  return (
    <main className="m-2 flex flex-1 flex-col items-stretch justify-center gap-2 md:flex-row md:my-10">
      <section className="contents md:flex md:flex-col gap-2 flex-1 md:max-w-2xl">
        <GoToPlaygroundModal className="grid min-h-0 w-full flex-1/2 basis-0 grid-cols-2 rounded bg-zinc-800" />
      </section>
      <section className="contents md:flex md:flex-col gap-2 flex-1 md:max-w-2xl">
        <ClassesWidget className="flex min-h-0 flex-1/2 basis-0 flex-col rounded bg-zinc-800 p-2" />
      </section>
    </main>
  );
}
