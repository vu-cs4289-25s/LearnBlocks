import { Button, Checkbox, Label, TextInput } from 'flowbite-react';
import { Link } from 'react-router-dom';

export function RegisterForm() {
  return (
    <form className="flex w-96 flex-col gap-4">
      <div>
        <div className="mb-2 block">
          <Label htmlFor="firstname" value="Your first name" />
        </div>
        <TextInput
          id="firstname"
          type="text"
          placeholder="john"
          required
          shadow
        />
      </div>
      <div>
        <div className="mb-2 block">
          <Label htmlFor="lastname" value="Your last name" />
        </div>
        <TextInput
          id="lastname"
          type="text"
          placeholder="doe"
          required
          shadow
        />
      </div>
      <div>
        <div className="mb-2 block">
          <Label htmlFor="username" value="Your username" />
        </div>
        <TextInput
          id="username"
          type="text"
          placeholder="johndoe"
          required
          shadow
        />
      </div>
      <div>
        <div className="mb-2 block">
          <Label htmlFor="email2" value="Your email" />
        </div>
        <TextInput
          id="email2"
          type="email"
          placeholder="name@netsblox.com"
          required
          shadow
        />
      </div>
      <div>
        <div className="mb-2 block">
          <Label htmlFor="password2" value="Your password" />
        </div>
        <TextInput id="password2" type="password" required shadow />
      </div>
      <div>
        <div className="mb-2 block">
          <Label htmlFor="repeat-password" value="Repeat password" />
        </div>
        <TextInput id="repeat-password" type="password" required shadow />
      </div>
      <div className="flex items-center gap-2">
        <Checkbox id="agree" />
        <Label htmlFor="agree" className="flex">
          I agree with the&nbsp;
          <Link
            href="/terms"
            className="text-cyan-600 hover:underline dark:text-cyan-500"
          >
            terms and conditions
          </Link>
        </Label>
      </div>
      <Button type="submit">Register new account</Button>
    </form>
  );
}
