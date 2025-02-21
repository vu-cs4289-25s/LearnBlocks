import { useNavigate } from 'react-router-dom';

/**
 * generates the form portion of the login card
 * @returns {import('react').ReactElement} Returns the value of x for the equation.
 */
export function LoginForm() {
  const navigate = useNavigate();
  const userId = 'temp';

  /**
   * @param {MouseEvent} e - the event triggered by the click
   */
  const onGithubLogin = (e) => {
    e.preventDefault();
    navigate('/students/home/' + userId);
  };

  return (
    <form className="flex w-96 flex-col gap-4">
      <section>
        <div htmlFor="username" value="Your username" />
        <div id="username" type="text" placeholder="username" required />
      </section>
      <section>
        <div htmlFor="password2" value="Your password" />
        <div id="password2" type="password" required />
      </section>
      <section className="flex flex-1 flex-col gap-2 align-middle">
        <div type="submit">Login</div>
        <div className="w-20 self-center" color="dark" onClick={onGithubLogin}>
          <div />
        </div>
      </section>
    </form>
  );
}
