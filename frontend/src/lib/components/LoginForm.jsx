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
  const userId = 'temp';

  const onGithubLogin = (e) => {
    e.preventDefault();
    navigate('/students/home/' + userId);
  };

  const onLogin = (e) => {
    e.preventDefault();
    navigate('/students/home/' + userId);
  };

  return (
    <form className="flex flex-col items-center gap-4 rounded-2xl bg-zinc-800 p-4">
      <img src="learnblocks.svg" alt="Learn Blocks Logo" />
      <h1 className="text-center text-2xl font-bold">Login</h1>
      <Field className="flex flex-col">
        <Label> username: </Label>
        <Input name="username" className="rounded bg-zinc-900 p-1" />
      </Field>
      <Field className="flex flex-col">
        <Label> password: </Label>
        <Input name="password" className="rounded bg-zinc-900 p-1" />
      </Field>
      <Button
        type="submit"
        className="rounded-lg border border-gray-100 px-2 py-0.5 duration-100 bg-zinc-900 hover:not-active:-translate-y-0.5 hover:not-active:shadow shadow-black"
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
