import { Field, Label, Input, Checkbox, Button } from '@headlessui/react';
import { CheckIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

/**
 * @returns {import('react').ReactElement} the registration form for the registration page
 */
export default function EditProfileWidget() {
  const [checked, setChecked] = useState(false);

  const onSubmit = (e, type) => {
    e.preventDefault()
  }

  return (
    <form className="flex w-96 flex-col gap-4 rounded-xl bg-zinc-800 p-8">
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
          name="repeat-password"
          type="password"
          required
          className="rounded bg-zinc-900 p-1"
        />
      </Field>

      <Field className="flex flex-row justify-between ">
        <Button
          type="submit"
          className="rounded-full border border-gray-100 bg-zinc-900 p-1 shadow-black duration-100 hover:not-active:-translate-y-0.5 hover:not-active:shadow flex-1/2"
          onClick={(e) => onSubmit(e, 'teacher')}
        >
          Save
        </Button>
      </Field>
    </form>
  );
}
