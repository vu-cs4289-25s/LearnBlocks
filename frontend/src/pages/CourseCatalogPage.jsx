import CatalogWidget from '$lib/components/CatalogWidget';

export default function CourseCatalogPage() {
  return (
    <main className="flex flex-1 flex-row">
      <CatalogWidget
        className={
          'm-2 flex flex-1 flex-col justify-between rounded bg-zinc-800 p-2'
        }
      />
    </main>
  );
}
