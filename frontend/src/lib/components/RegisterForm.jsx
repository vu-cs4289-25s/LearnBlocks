import { Link } from 'react-router-dom';

export function RegisterForm() {
  return (
    <form className="flex w-96 flex-col gap-4">
      <div>
        <div className="mb-2 block">
          <div htmlFor="firstname" value="Your first name" />
        </div>
        <div id="firstname" type="text" placeholder="john" required />
      </div>
      <div>
        <div className="mb-2 block">
          <div htmlFor="lastname" value="Your last name" />
        </div>
        <div id="lastname" type="text" placeholder="doe" required />
      </div>
      <div>
        <div className="mb-2 block">
          <div htmlFor="username" value="Your username" />
        </div>
        <div id="username" type="text" placeholder="johndoe" required />
      </div>
      <div>
        <div className="mb-2 block">
          <div htmlFor="email2" value="Your email" />
        </div>
        <div
          id="email2"
          type="email"
          placeholder="name@netsblox.com"
          required
        />
      </div>
      <div>
        <div className="mb-2 block">
          <div htmlFor="password2" value="Your password" />
        </div>
        <div id="password2" type="password" required />
      </div>
      <div>
        <div className="mb-2 block">
          <div htmlFor="repeat-password" value="Repeat password" />
        </div>
        <div id="repeat-password" type="password" required />
      </div>
      <div className="flex items-center gap-2">
        <div id="agree" />
        <div htmlFor="agree" className="flex">
          I agree with the&nbsp;
          <Link
            to="/terms"
            className="text-primary-500 hover:text-primary-400 hover:underline"
          >
            terms and conditions
          </Link>
        </div>
      </div>

      <div type="submit">Register new account</div>
    </form>
  );
}
