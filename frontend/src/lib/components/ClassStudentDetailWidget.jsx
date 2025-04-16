import { useParams, Link } from "react-router-dom";

export default function ClassStudentDetailWidget({ className }) {
  const { classid, studentid } = useParams();

  const student = {
    name: "Joe Johnson",
    email: "joe@example.com",
  };

  const courses = [
    ["Course 1", "Complete", 5],
    ["Course 2", "Complete", 3],
    ["Course 3", "In Progress", 2],
    ["Course 4", "Not Started", 0],
    ["Course 5", "Not Started", 0],
  ];

  const projects = [
    ["Project A", "90%"],
    ["Project B", "75%"],
    ["Project C", "Incomplete"],
  ];

  return (
    <section className={className}>
      <div className="flex flex-col items-center text-white mb-6">
        <h1 className="text-2xl font-bold">{student.name}</h1>
        <p className="text-sm text-zinc-400">{student.email}</p>
      </div>
      <div className="mt-4 flex flex-col gap-4 md:flex-row">
        <div className="flex flex-1 flex-col rounded bg-zinc-900 p-2">
          <h2 className="mb-2 text-lg font-semibold text-white">Courses</h2>
          <table className="w-full text-sm text-zinc-300">
            <thead className="border-b border-zinc-700 text-zinc-400 text-xs uppercase">
              <tr>
                <th className="py-2 px-2 text-left">Title</th>
                <th className="py-2 px-2 text-left">Status</th>
                <th className="py-2 px-2 text-left">Badges</th>
              </tr>
            </thead>
            <tbody>
              {courses.map(([title, status, badges], i) => (
                <tr key={i} className="border-b border-zinc-800">
                  <td className="py-2 px-2">{title}</td>
                  <td className="py-2 px-2">
                    <span className={`rounded px-2 py-0.5 text-xs font-medium text-white ${
                      status === "Complete" ? "bg-blue-600" :
                      status === "In Progress" ? "bg-purple-600" :
                      "bg-zinc-600"
                    }`}>
                      {status}
                    </span>
                  </td>
                  <td className="py-2 px-2">{badges}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex flex-1 flex-col rounded bg-zinc-900 p-2">
          <h2 className="mb-2 text-lg font-semibold text-white">Projects</h2>
          <table className="w-full text-sm text-zinc-300">
            <thead className="border-b border-zinc-700 text-zinc-400 text-xs uppercase">
              <tr>
                <th className="py-2 px-2 text-left">Title</th>
                <th className="py-2 px-2 text-left">Score</th>
              </tr>
            </thead>
            <tbody>
              {projects.map(([title, score], i) => (
                <tr key={i} className="border-b border-zinc-800">
                  <td className="py-2 px-2">{title}</td>
                  <td className="py-2 px-2">{score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="mt-6 flex justify-center">
        <Link
          to={`/t/classes/${classid}/students`}
          className="transition-color w-40 rounded-full border border-amber-400 text-center px-3 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
        >
          Back
        </Link>
      </div>
    </section>
  );
}
