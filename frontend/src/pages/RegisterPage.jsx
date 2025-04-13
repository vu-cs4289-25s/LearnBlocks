import RegisterForm from '$lib/components/RegisterForm';

export default function RegistrationPage() {
  return (
    <main className="flex flex-1 flex-row items-center justify-evenly ">
      <figure className="flex flex-col gap-10 max-md:hidden">
        <img
          src="learnblocks.svg"
          className="h-60 "
          alt="Learn Blocks Logo"
        />
        <h1 className="text-center text-4xl font-bold dark:text-zinc-100">
          LearnBlox
        </h1>
      </figure>
        <RegisterForm />
    </main>
  );
}
