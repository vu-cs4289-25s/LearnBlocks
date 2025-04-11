import CatalogWidget from "$lib/components/CatalogWidget";

export default function CourseCatalogPage() {
  return (
    <main className="flex flex-1 flex-row justify-center md:my-10">
      <CatalogWidget className="m-2 flex flex-1 flex-col justify-between rounded bg-zinc-800 p-4 max-w-5xl" />
    </main>
  );
}
