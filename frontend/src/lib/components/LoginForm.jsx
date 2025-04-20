import GithubIcon from "$lib/assets/github-icon";
import { Button, Field, Label } from "@headlessui/react";
import { useNavigate } from "react-router-dom";
import { Input } from "@headlessui/react";
import { useContext, useRef } from "react";
import { AuthUserContext, ErrorContext } from "$lib/contexts/ErrorContext";
import { fetchUser, tryLogin } from "$lib/utils/actions.mjs";

/**
 * generates the form portion of the login card
 * @returns {import('react').ReactElement} Returns the form element.
 */
export function LoginForm() {
  const navigate = useNavigate();
  const { setError } = useContext(ErrorContext);
  const { setAuthUser } = useContext(AuthUserContext);
  const formRef = useRef(null);

  const onGithubLogin = (e) => {
    e.preventDefault();
    setError("GitHub login not implemented");
  };

  const onLogin = async (e) => {
    e.preventDefault();
    const rawFormData = new FormData(formRef.current);
    const data = Object.fromEntries(rawFormData.entries());
    const res = await tryLogin(data);
    if (res instanceof Error) return setError(res.message);
    //console.log(data);
    const user = await fetchUser(res,data.username);
    console.log(user);
    setAuthUser({...res,...user});
    navigate(`/${user.role[0]}/home`);
  };

  return (
    <form
      ref={formRef}
      className="flex flex-col items-center gap-4 rounded-2xl bg-zinc-800 p-9"
    >
      <img src="learnblocks.svg" alt="Learn Blocks Logo" />
      <h1 className="text-center text-2xl font-bold">Login</h1>
      <Field className="flex flex-col w-80">
        <Label> username: </Label>
        <Input name="username" className="rounded bg-zinc-900 p-1" required />
      </Field>
      <Field className="flex flex-col w-80">
        <Label> password: </Label>
        <Input name="password" type="password" className="rounded bg-zinc-900 p-1" required />
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
