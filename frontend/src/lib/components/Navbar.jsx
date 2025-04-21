import { Link, useNavigate } from "react-router-dom";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { useContext, useState } from "react";
import { Button } from "@headlessui/react";
import { AuthUserContext, ErrorContext } from "$lib/contexts/Context";

/**
 * @param {object} param0 : Props for the Navbar
 * @param {import('$lib/types/common.mjs').NavLinkType[]} param0.navLinkData : Navbar link data to populate links
 * @returns {import('react').ReactElement} The navbar element
 */

const loggedOutLinks = { register: "/register", login: "/login" };
const studentLinks = {
  home: "/s/home",
  catalog: "/catalog",
  // courses: "/s/courses",
  // classes: "/s/classes",
};
const teacherLinks = {
  home: "/t/home",
  catalog: "/catalog",
  classes: "/t/classes",
};

function getLinks(authUser) {
  if (!authUser) return loggedOutLinks;
  else if (authUser.role === "student") return studentLinks;
  else return teacherLinks;
}

export default function Navbar({ navLinkData }) {
  const [closed, setClosed] = useState(true);
  const navigate = useNavigate();

  const { authUser, setAuthUser } = useContext(AuthUserContext);
  const { setError } = useContext(ErrorContext)

  const links = getLinks(authUser);

  const handleLogout = async (e) => {
    const res = await tryLogout(authUser);
    setClosed(true);
    if (res instanceof Error) {
      return setError(res.message);
    }
    setAuthUser(null);
    navigate("/");
  };

  return (
    <nav className="flex flex-row flex-wrap items-center px-2 py-2 dark:bg-zinc-800">
      <Link to="/" className="flex flex-1/2 flex-row items-center">
        <img
          src="/learnblocks.svg"
          className="mr-3 h-9"
          alt="Learn Blocks Logo"
        />
        LearnBlox
      </Link>
      <div className="flex flex-1/2 flex-row justify-end md:hidden">
        <Button onClick={() => setClosed(false)}>
          <Bars3Icon title="Expand Navbar" className="h-8 cursor-pointer" />
        </Button>
      </div>

      <ul
        className={`flex flex-1 flex-col gap-2 bg-zinc-800 px-2 py-1 text-center max-md:absolute max-md:top-0 max-md:left-0 max-md:h-screen max-md:w-screen md:max-h-fit md:flex-1/2 md:flex-row md:justify-end md:text-xs z-10 ${closed ? "max-md:hidden" : ""} `}
      >
        <li className="flex flex-row items-center justify-between md:hidden ">
          <Link src="/learnblocks.svg" to="/" onClick={() => setClosed(true)}>
            <img
              src="/learnblocks.svg"
              className="mr-3 h-9"
              alt="Learn Blocks Logo"
            />
          </Link>
          <Button onClick={() => setClosed(true)}>
            <XMarkIcon className="h-8 cursor-pointer" alt="close navigation " />
          </Button>
        </li>
        {Object.entries(links).map(([name, to], key) => {
          return (
            <div key={key}>
              <Link to={to} onClick={() => setClosed(true)}>
                {name}
              </Link>
              <hr  className="text-zinc-600 md:hidden" />
            </div>
          );
        })}
        {!links.login ? (
          <>
            <Link to="/" onClick={handleLogout}>
              logout
            </Link>
          </>
        ) : null}
      </ul>
    </nav>
  );
}
