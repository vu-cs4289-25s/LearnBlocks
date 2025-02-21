import ActivityWidget from '$lib/components/ActivityWidget'; 

export default function StudentHomePage() {
  return (
    <main className="flex flex-1 flex-col p-2 gap-2 dark:bg-gray-900 md:p-10">
      <ActivityWidget/>
      <div className='flex-1'>this</div>
      <div className="flex-1">this</div>
    </main>
  );
}
