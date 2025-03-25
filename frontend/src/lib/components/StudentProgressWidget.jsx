import { Link } from 'react-router-dom';

const data = [
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
  ['student1', 'progress1'],
];
export default function StudentProgressWidget({ className }) {
  return (
    <section className={className}>
      <h1 className="text-xl font-bold"> Current Module</h1>
      <hr className="text-zinc-400" />
      <ul className="flex flex-col gap-2 overflow-auto rounded border-6 border-zinc-900 bg-zinc-900 p-2">
        {data.map((entry, key) => (
          <li
            key={key}
            className="flex flex-row justify-between rounded bg-zinc-800 p-2 text-zinc-500"
          >
            <h2>{entry[0]}</h2>
            <h2>{entry[1]}</h2>
          </li>
        ))}
      </ul>
      <Link
        className="transition-color my-1 w-1/2 self-center rounded-full border-2 border-amber-400 text-center shadow-amber-300/50 duration-100 hover:bg-amber-400 hover:shadow active:bg-amber-500"
        to="/t/classes"
      >
        Manage Classes
      </Link>
    </section>
  );
}
