import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center dark:bg-zinc-900">
      <img
        src="learnblocks.svg"
        className="h-50 pb-10"
        alt="Learn Blocks Logo"
      />
      <h1 className="text-center text-4xl font-bold dark:text-white">
        LearnBlox
      </h1>
      <h2 className="p-2 text-center text-xl font-bold dark:text-white">
        An Interactive Approach To Learning Code
      </h2>
      <Link
        to={'/register'}
        className="transition-color rounded-full border-2 border-amber-700 p-2 shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800 "
      >
        Get Started
      </Link>
    </main>
  );
}
