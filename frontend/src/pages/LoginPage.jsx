import { LoginForm } from '$lib/components/LoginForm';

export default function LoginPage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-evenly dark:bg-zinc-900">
      <LoginForm />
    </main>
  );
}
