import EditProfileWidget from "$lib/components/EditProfileWidget";

export default function EditProfilePage() {
  return (
    <main className="flex flex-1 flex-row items-center justify-evenly ">
      <figure className="flex flex-col gap-10 max-md:hidden">
        <img
          src="/learnblocks.svg"
          className="h-60 "
          alt="Learn Blocks Logo"
        />
        <h1 className="text-center text-4xl font-bold dark:text-zinc-100">
          LearnBlocks
        </h1>
      </figure>
        <EditProfileWidget/>
    </main>
  );
}
