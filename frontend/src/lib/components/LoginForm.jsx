import GithubIcon from '$lib/assets/github-icon';
import { Button, Field, Label } from '@headlessui/react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@headlessui/react';

/**
 * generates the form portion of the login card
 * @returns {import('react').ReactElement} Returns the value of x for the equation.
 */
export function LoginForm() {
  const navigate = useNavigate();

  const onGithubLogin = (e) => {
    e.preventDefault();
    navigate('/s/home');
  };

  const onLogin = (e) => {
    e.preventDefault();
    navigate('/s/home');
  };

  return (
    <form className="flex flex-col items-center gap-4 rounded-2xl bg-zinc-800 p-4">
      <img src="learnblocks.svg" alt="Learn Blocks Logo" />
      <h1 className="text-center text-2xl font-bold">Login</h1>
      <Field className="flex flex-col">
        <Label> username: </Label>
        <Input name="username" className="rounded bg-zinc-900 p-1" required />
      </Field>
      <Field className="flex flex-col">
        <Label> password: </Label>
        <Input name="password" className="rounded bg-zinc-900 p-1" required />
      </Field>
      <Button
        type="submit"
        className="rounded-full border self-stretch  border-gray-100 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:-translate-y-0.5 hover:not-active:shadow"
        onClick={onLogin}
      >
        login
      </Button>
      <Button className="w-fit" onClick={onGithubLogin}>
        <GithubIcon />
      </Button>
    </form>
  );
}
