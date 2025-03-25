import ActivityWidget from '$lib/components/ActivityWidget';
import BadgeWidget from '$lib/components/BadgeWidget';
import GoToPlaygroundModal from '$lib/components/GoToPlaygroundModal';
import NextModuleModal from '$lib/components/NextModuleModal';

export default function StudentHomePage() {
  return (
    <main className="flex max-w-96 flex-1 flex-col items-center justify-evenly gap-2 self-center p-2 md:my-20 md:max-w-6xl md:flex-row md:items-stretch md:gap-4 ">
      <section className="max-md:contents md:flex md:flex-1/2 md:flex-col md:w-1/2 md:gap-4">
        <ActivityWidget className="flex w-full flex-col justify-start gap-2 rounded bg-zinc-800 p-2" />
        <BadgeWidget className="hidden md:flex md:w-full md:flex-col md:justify-start md:gap-2 rounded bg-zinc-800 p-2" />
        <NextModuleModal className="flex w-full flex-1 basis-0 flex-col rounded bg-zinc-800 p-2 md:order-3" />
      </section>
      <section className="max-md:contents md:flex md:flex-1/2 md:flex-col md:w-1/2">
        <GoToPlaygroundModal className="grid min-h-0 w-full flex-1 basis-0 grid-cols-2 rounded bg-zinc-800 " />
      </section>
    </main>
  );
}
