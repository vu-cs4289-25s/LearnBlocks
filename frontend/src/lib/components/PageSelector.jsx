import { Button } from "@headlessui/react"; 

export default function PageSelector({page, setPage, arr}) {
  return (
    <ul className="mt-2 flex flex-row justify-between gap-2 rounded-full">
      <li className={`${page === 1 ? 'invisible' : 'visible'} `}>
        <Button
          onClick={() => setPage(page - 1)}
          className="rounded-full bg-zinc-700 px-2"
        >
          {'<'}
        </Button>
      </li>
      <li className="rounded-full bg-zinc-700 px-2">
        <Button>
          {page} of {arr.length}
        </Button>
      </li>
      <li className={`${page === arr.length ? 'invisible' : 'visible'} `}>
        <Button
          onClick={() => setPage(page + 1)}
          className="rounded-full bg-zinc-700 px-2"
        >
          {'>'}
        </Button>
      </li>
    </ul>
  );
}
