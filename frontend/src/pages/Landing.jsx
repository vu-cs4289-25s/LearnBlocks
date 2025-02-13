import { Button } from 'flowbite-react';

export default function LandingPage() {
  return (
    <main className="dark:bg-nb-gray-300 flex flex-1 flex-col items-center justify-center">
      <img
        src="learnblocks.svg"
        className="h-50 pb-10"
        alt="Learn Blocks Logo"
      />
      <h1 className="text-center text-4xl font-bold dark:text-white">
        LearnBlox        
      </h1>
      <h2 className="p-2 text-center text-xl font-bold dark:text-white">
        An Interactive approach to learning code
      </h2>
      <Button pill color="yellow">
        Get Started
      </Button>
    </main>
  );
}
