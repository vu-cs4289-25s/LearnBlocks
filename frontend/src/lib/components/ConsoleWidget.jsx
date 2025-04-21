const Arrow = '\u{25B6}';
const Gap = ' ';

export default function ConsoleWidget({ className, logs }) {

  return (
    <section className={className}>
      <h1 className="text-xl font-bold">Output</h1>
      <hr className="text-zinc-600" />
      <ul className="m-2 flex flex-1 flex-col justify-end gap-1 rounded bg-zinc-900 p-2 font-mono text-lg">
        {logs.map((log, key) => (
          <li key={key}>{Arrow + Gap + log}</li>
        ))}
      </ul>
    </section>
  );
}
