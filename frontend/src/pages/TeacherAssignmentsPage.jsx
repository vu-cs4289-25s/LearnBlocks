const myClass = 'this';

export default function TeacherAssignmentsPage() {
  return (
    <main className="flex w-full max-w-md flex-1 flex-col items-stretch justify-evenly gap-2 self-center p-2 md:my-20 md:max-w-6xl md:flex-row md:items-stretch md:gap-4">
      <section className="flex flex-1 flex-col rounded bg-zinc-800 p-1">
        <h1> Assignments </h1>
        <hr className="text-zinc-500" />
      </section>
    </main>
  );
}
