import { useParams, Link } from "react-router-dom";

/**
 * @param {object} props
 * @param {string} props.className
 * @param {Array<{name: string, email: string, role: string}>} [props.students]
 */
export default function StudentsListWidget({ className, students = [] }) {
  const { classid } = useParams();

  // Generate 20 mock students if no data is passed in
  const defaultStudents = Array.from({ length: 20 }, (_, i) => ({
    name: `Student ${i + 1}`,
    email: `student${i + 1}@example.com`,
    role: i === 0 ? "Owner" : "Participant",
  }));

  const studentList = students.length > 0 ? students : defaultStudents;

  return (
    <section className={className}>
      <h1 className="text-xl font-bold text-white">Students in Class {classid}</h1>
      <hr className="text-zinc-400 mb-2" />

      <div className="rounded border-6 border-zinc-900 bg-zinc-900">
        <div className="flex px-3 py-2 text-xs font-semibold uppercase text-zinc-400 border-b border-zinc-700">
          <div className="w-1/4">Name</div>
          <div className="w-1/3">Email</div>
          <div className="w-1/4">Role</div>
          <div className="w-1/6 text-right"></div>
        </div>
        <div className="max-h-[400px] overflow-y-auto">
          {studentList.map((student, idx) => (
            <div
              key={idx}
              className="flex items-center px-3 py-2 border-b border-zinc-800 hover:bg-zinc-800/50 text-sm text-zinc-300"
            >
              <div className="w-1/4 font-medium">{student.name}</div>
              <div className="w-1/3 text-xs text-zinc-400">{student.email}</div>
              <div className="w-1/4">{student.role}</div>
              <div className="w-1/6 text-right">
                <Link
                  to={`/t/classes/${classid}/students/${idx}`}
                  className="rounded bg-amber-400 px-3 py-1 text-xs font-medium text-black hover:bg-amber-500"
                >
                  View
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      <Link
        className="transition-color mt-4 w-40 self-center rounded-full border border-amber-400 text-center px-3 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
        to="/t/home"
      >
        Back to Home
      </Link>
    </section>
  );
}
