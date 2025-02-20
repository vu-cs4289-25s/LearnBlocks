import { Card } from 'flowbite-react';
import { LoginForm } from '$lib/components/LoginForm';

export default function LoginPage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-evenly dark:bg-gray-900">
      <Card className="flex flex-col">
        <figure className="flex flex-col">
          <img
            src="learnblocks.svg"
            className="scale-75 "
            alt="Learn Blocks Logo"
          />
          <h1 className="text-center text-4xl font-bold dark:text-white">
            LearnBlox
          </h1>
        </figure>
        <LoginForm />
      </Card>
    </main>
  );
}
