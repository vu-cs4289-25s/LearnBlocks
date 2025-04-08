import { useParams, Link } from "react-router-dom";

export default function ClassStudentDetailWidget({ className }) {
  const { classid, studentid } = useParams();

  const student = {
    name: "Joe Johnson",
    email: "Joe@example.com",
  };

  const lessons = [
    ["Lesson 1", "Complete"],
    ["Lesson 2", "Complete"],
    ["Lesson 3", "In Progress"],
    ["Lesson 4", "Not Started"],
    ["Lesson 5", "Not Started"],
  ];

  const projects = [
    ["Project A", "90%"],
    ["Project B", "75%"],
    ["Project C", "Incomplete"],
  ];

  return (
    <section className={className}>
      <div className="flex flex-col items-center text-white">
        <h1 className="text-2xl font-bold mt-2">{student.name}</h1>
        <p className="text-sm text-zinc-400">{student.email}</p>
      </div>

      <div className="mt-6 flex flex-col gap-4 md:flex-row">
        {/* Lessons */}
        <div className="flex-1 rounded bg-zinc-900 p-4">
          <h2 className="mb-2 text-lg font-semibold text-white">Lessons</h2>
          <table className="w-full text-sm text-zinc-300">
            <tbody>
              {lessons.map(([title, status], i) => (
                <tr key={i} className="border-b border-zinc-700">
                  <td className="py-1">{title}</td>
                  <td className="py-1">
                    <span className={`rounded px-2 py-0.5 text-xs ${
                      status === "Complete" ? "bg-blue-600" :
                      status === "In Progress" ? "bg-purple-600" :
                      "bg-zinc-600"
                    } text-white`}>
                      {status}
                    </span>
                  </td>
                  <td className="py-1 text-right">
                    <button className="text-amber-400 hover:underline">view</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Projects */}
        <div className="flex-1 rounded bg-zinc-900 p-4">
          <h2 className="mb-2 text-lg font-semibold text-white">Projects</h2>
          <table className="w-full text-sm text-zinc-300">
            <tbody>
              {projects.map(([title, score], i) => (
                <tr key={i} className="border-b border-zinc-700">
                  <td className="py-1">{title}</td>
                  <td className="py-1">{score}</td>
                  <td className="py-1 text-right">
                    <button className="text-amber-400 hover:underline">view</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-6 flex justify-center">
        <Link
          to={`/t/classes/${classid}/students`}
          className="transition-color w-40 rounded-full border border-amber-400 text-center px-3 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500">
          Back
        </Link>
      </div>
    </section>
  );
}
