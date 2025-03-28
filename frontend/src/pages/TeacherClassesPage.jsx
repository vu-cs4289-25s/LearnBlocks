import ClassesWidget from "$lib/components/ClassesWidget";

export default function TeacherClassesPage() {
  return (
    <main className="flex flex-1 flex-row justify-center md:my-10">
      <ClassesWidget
        className={
          'm-2 flex flex-1 flex-col justify-between rounded bg-zinc-800 p-2 max-w-4xl'
        }
      />
    </main>
  );
}
