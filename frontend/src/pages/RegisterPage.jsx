import { Card } from 'flowbite-react';
import { RegisterForm } from '$lib/components/RegisterForm';

export default function RegistrationPage() {
  return (
    <main className="flex flex-1 flex-row items-center justify-evenly dark:bg-gray-900">
      <figure className="flex flex-col">
        <img
          src="learnblocks.svg"
          className="h-80 pb-10"
          alt="Learn Blocks Logo"
        />
        <h1 className="text-center text-4xl font-bold dark:text-white">
          LearnBlox
        </h1>
      </figure>
      <Card>
        <RegisterForm />
      </Card>
    </main>
  );
}
