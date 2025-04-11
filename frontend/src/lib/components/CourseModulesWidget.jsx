import { Link, useParams } from "react-router-dom";

export default function CourseModulesWidget({ className }) {
  const { courseid } = useParams();

  const modules = [
    { id: 0, title: "Module 1", description: "Introduction to the course", status: "Completed" },
    { id: 1, title: "Module 2", description: "Core concepts and lessons", status: "In Progress" },
    { id: 2, title: "Module 3", description: "Advanced topics and projects", status: "Not Started" },
    { id: 3, title: "Module 4", description: "Final review and assessment", status: "Not Started" },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case "Completed":
        return "bg-blue-600";
      case "In Progress":
        return "bg-purple-600";
      case "Not Started":
      default:
        return "bg-zinc-600";
    }
  };

  return (
    <section className={className}>
      <h1 className="text-2xl font-bold text-white mb-4">Modules for Course {courseid}</h1>
      <ul className="flex flex-col gap-2">
        {modules.map((mod) => (
          <li
            key={mod.id}
            className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 rounded bg-zinc-900 p-4 text-zinc-300 hover:bg-zinc-800 transition"
          >
            <div>
              <h2 className="text-lg font-semibold text-white">{mod.title}</h2>
              <p className="text-sm text-zinc-400">{mod.description}</p>
            </div>

            <div className="flex gap-2 items-center self-end md:self-auto">
              <span
                className={`rounded px-2 py-0.5 text-xs text-white ${getStatusColor(
                  mod.status
                )}`}
              >
                {mod.status}
              </span>

              <Link
                to={`/catalog/${courseid}/module/${mod.id}`}
                className="rounded bg-amber-400 px-3 py-1 text-xs font-medium text-black hover:bg-amber-500"
              >
                Enter
              </Link>
            </div>
          </li>
        ))}
      </ul>

      <div className="mt-6 flex justify-center">
        <Link
          to="/catalog"
          className="transition-color w-40 rounded-full border border-amber-400 text-center px-3 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
        >
          Back to Catalog
        </Link>
      </div>
    </section>
  );
}
