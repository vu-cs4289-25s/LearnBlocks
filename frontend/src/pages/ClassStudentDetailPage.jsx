import ClassStudentDetailWidget from "$lib/components/ClassStudentDetailWidget";

export default function ClassStudentDetailPage() {
  return (
    <main className="flex flex-1 flex-row justify-center md:my-10">
      <ClassStudentDetailWidget
        className="m-2 flex flex-1 flex-col justify-between rounded bg-zinc-800 p-2 max-w-5xl"
      />
    </main>
  );
}
