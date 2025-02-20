import { Button, Label, TextInput } from 'flowbite-react';
import { Github } from 'flowbite-react-icons/solid'
/**
 * generates the form portion of the login card
 * @returns {import('react').ReactElement} Returns the value of x for the equation.
 */
export function LoginForm() {
  return (
    <form className="flex w-96 flex-col gap-4">
      <section>
        <Label htmlFor="username" value="Your username" />
        <TextInput
          id="username"
          type="text"
          placeholder="username"
          required
          shadow
        />
      </section>
      <section>
        <Label htmlFor="password2" value="Your password" />
        <TextInput id="password2" type="password" required shadow />
      </section>
      <section className='flex flex-1 flex-col align-middle gap-2'>
        <Button pill type="submit">
          Login
        </Button>
        <Button pill className="w-20 self-center" color='dark'>
          <Github/>
        </Button>
      </section>
    </form>
  );
}
