import { useParams, Link } from "react-router-dom";
import courses from "$lib/courses";

export default function ModuleWidget({ className }) {
    const { courseid, moduleid } = useParams();
    const course = courses.find((c) => c.id === courseid);
    const module = course?.modules?.[moduleid];

    const getStatusColor = (status) => {
        switch (status) {
            case "Completed":
                return "bg-blue-600";
            case "In Progress":
                return "bg-green-600";
            case "Not Started":
            default:
                return "bg-zinc-600";
        }
    };

    if (!course || !module) {
        return (
            <section className={className}>
                <h1 className="text-xl text-white">Module not found</h1>
            </section>
        );
    }

    return (
        <section className={`${className} grid grid-cols-1 md:grid-cols-2 gap-4`}>
            <div className="flex flex-col gap-4">
                <div className={`flex justify-between items-center rounded px-4 py-2 ${getStatusColor(module.status)}`}>
                    <h1 className="text-2xl font-extrabold text-white">{course.name}</h1>
                    <span className="text-white text-sm font-semibold">{module.status}</span>
                </div>
                <div className="flex flex-col justify-between gap-4 rounded bg-zinc-800 p-4 h-full">
                    <div>
                        <h2 className="text-xl font-bold text-white">{module.title}</h2>
                        <p className="text-sm text-zinc-300 whitespace-pre-line mt-2">
                            {module.instructions}
                        </p>
                    </div>

                    <div className="mt-4 flex justify-between">
                        <Link
                            to={`/catalog/${courseid}`}
                            className="transition-color rounded-full border border-amber-400 px-4 py-1 text-sm text-white shadow-sm duration-100 hover:bg-amber-400 hover:text-black hover:shadow-md active:bg-amber-500"
                        >
                            Back to Modules
                        </Link>
                        <button className="rounded bg-amber-400 px-4 py-1 text-sm font-medium text-black hover:bg-amber-500">
                            Submit
                        </button>
                    </div>
                </div>
            </div>
            <div className="flex flex-col gap-4">
                <div className="rounded bg-zinc-800 p-4 text-center text-zinc-400">Blockly Editor Placeholder</div>
                <div className="rounded bg-zinc-800 p-4 text-center text-zinc-400">Terminal Placeholder</div>
            </div>
        </section>
    );
}