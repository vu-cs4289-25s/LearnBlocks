import { useParams, Link } from "react-router-dom";

const mockStudents = [
  ["Student 1", "student1@example.com"],
  ["Student 2", "student2@example.com"],
  ["Student 3", "student3@example.com"],
  ["Student 4", "student4@example.com"],
  ["Student 5", "student5@example.com"],
];

export default function StudentsListWidget({ className }) {
  const { classid } = useParams();

  return (
    <section className={className}>
      <h1 className="text-xl font-bold text-white">Students in Class {classid}</h1>
      <hr className="text-zinc-400" />

      <ul className="flex flex-col gap-2 overflow-auto rounded border-6 border-zinc-900 bg-zinc-900 p-2">
        {mockStudents.map(([name, email], key) => (
          <li
            key={key}
            className="flex flex-row justify-between rounded bg-zinc-800 p-2 text-zinc-300"
          >
            <div>
              <h2 className="font-semibold">{name}</h2>
              <p className="text-xs text-zinc-400">{email}</p>
            </div>

            <Link
              to={`/t/classes/${classid}/students/${key}`}
              className="self-center rounded bg-amber-400 px-3 py-1 text-xs font-medium text-black hover:bg-amber-500"
            >
              View
            </Link>
          </li>
        ))}
      </ul>

      <Link
        className="transition-color my-1 w-1/2 self-center rounded-full border-2 border-amber-400 text-center shadow-amber-300/50 duration-100 hover:bg-amber-400 hover:shadow active:bg-amber-500 text-white"
        to="/t/classes"
      >
        Back to Classes
      </Link>
    </section>
  );
}
