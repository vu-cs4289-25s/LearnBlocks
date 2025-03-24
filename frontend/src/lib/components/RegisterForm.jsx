import { ErrorContext } from "$lib/contexts/ErrorContext";
import { Field, Label, Input, Checkbox, Button } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/24/outline";
import { useContext, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { tryRegister } from "$lib/utils/actions.mjs";

/**
 * @returns {ReactElement} the registration form for the registration page
 */
export default function RegisterForm() {
  const [checked, setChecked] = useState(false);
  const { setError } = useContext(ErrorContext);
  const navigate = useNavigate();

  const formRef = useRef(null);

  const onSubmit = async (e, type) => {
    e.preventDefault();
    const rawFormData = new FormData(formRef.current);
    rawFormData.set("type", type);
    const res = await tryRegister(Object.fromEntries(rawFormData.entries()));
    if (res instanceof Error) setError(res.message);
    else navigate("/login");
  };

  return (
    <form
      className="flex w-96 flex-col gap-4 rounded-xl bg-zinc-800 p-8"
      ref={formRef}
    >
      <Field className="flex flex-col">
        <Label> First Name: </Label>
        <Input
          name="first_name"
          type="text"
          placeholder="john"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field className="flex flex-col">
        <Label> Last Name: </Label>
        <Input
          name="last_name"
          type="text"
          placeholder="doe"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field className="flex flex-col">
        <Label> Username: </Label>
        <Input
          name="username"
          type="text"
          placeholder="johndoe"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field className="flex flex-col">
        <Label> Email:</Label>
        <Input
          name="email"
          type="email"
          placeholder="abc@d.com"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field className="flex flex-col">
        <Label> Password:</Label>
        <Input
          name="password"
          type="password"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field className="flex flex-col">
        <Label className="block"> Repeat Password: </Label>
        <Input
          name="repeatPassword"
          type="password"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>
      <Field>
        <Checkbox
          checked={checked}
          onChange={setChecked}
          name="terms"
          value="accept"
          className="transition-color mr-1.5 inline-block h-4 w-4 overflow-hidden rounded border border-zinc-100 bg-zinc-900 duration-100 data-[checked]:bg-amber-600"
        >
          <CheckIcon className={`${checked ? "visible" : "invisible"}`} />
        </Checkbox>
        <Label>
          I agree with the&nbsp;
          <Link
            to="/terms"
            className="hover:text-primary-400 inline-block text-amber-600 hover:underline"
          >
            terms and conditions.
          </Link>
        </Label>
      </Field>

      <Field className="flex flex-row justify-between gap-2">
        <Button
          type="submit"
          className="rounded-full border border-gray-100 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:-translate-y-0.5 hover:not-active:shadow flex-1/2"
          onClick={(e) => onSubmit(e, "student")}
        >
          I am a student
        </Button>

        <Button
          type="submit"
          className="rounded-full border border-amber-500 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:-translate-y-0.5 hover:not-active:shadow flex-1/2 text-amber-500"
          onClick={(e) => onSubmit(e, "teacher")}
        >
          I am a teacher
        </Button>
      </Field>
    </form>
  );
}
