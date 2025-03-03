import { Button } from '@headlessui/react';
import { Link } from 'react-router-dom';
import CourseWidget from './CourseWidget';

const example = {
  name: 'conditionals',
  modules: [
    { name: 'module 1', status: 'Complete', link: '/playground' },
    { name: 'module 2', status: 'Complete', link: '/playground' },
    { name: 'module 3', status: 'In Progress', link: '/playground' },
    { name: 'module 4', status: 'Locked', link: '' },
    { name: 'module 5', status: 'Locked', link: '' },
  ],
};
export default function NextModuleModal({ className }) {
  return (
    <section className={className}>
      <h1 className="text-xl font-bold">Recent Course</h1>
      <hr className="mb-2 text-center text-zinc-700" />
      <CourseWidget
        course={example}
        className="flex flex-1 flex-col rounded border-10 border-zinc-900 bg-zinc-900"
      />
      <section className="col-span-2 flex flex-col items-center justify-center gap-4">
        <Link className="transition-color w-1/2 rounded-full border-2 border-amber-700 text-center shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800">
          Browse Catalog
        </Link>
      </section>
    </section>
  );
}
