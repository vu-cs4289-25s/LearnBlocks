import { Card } from 'flowbite-react';
import ActivityWidget from '$lib/components/ActivityWidget'; 

export default function StudentHomePage() {
  return (
    <main className="flex flex-1 flex-col py-2 dark:bg-gray-900 md:p-10">
      <ActivityWidget className="">this</ActivityWidget>
      <Card className="">this</Card>
      <Card className="">this</Card>
    </main>
  );
}
