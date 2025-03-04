import { Link } from 'react-router-dom';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import { Button } from '@headlessui/react';

  /**
   * @param {object} param0 : Props for the Navbar  
   * @param {import('$lib/types/common.mjs').NavLinkType[]} param0.navLinkData : Navbar link data to populate links
   * @returns {import('react').ReactElement} The navbar element
   */
export default function Nav({ navLinkData }) {
  const [closed, setClosed] = useState(true);

  return (
    <nav className="flex flex-row flex-wrap items-center px-2 py-1 dark:bg-zinc-800">
      <Link to="/" className="flex flex-1/2 flex-row items-center">
        <img
          src="/learnblocks.svg"
          className="mr-3 h-9"
          alt="Learn Blocks Logo"
        />
        LearnBlocks
      </Link>
      <div className="flex flex-1/2 flex-row justify-end md:hidden">
        <Button onClick={() => setClosed(false)}>
          <Bars3Icon title="Expand Navbar" className="h-8 cursor-pointer" />
        </Button>
      </div>

      <ul
        className={`flex flex-1 flex-col gap-2 bg-zinc-800 px-2 py-1 text-center max-md:absolute max-md:top-0 max-md:left-0 max-md:h-screen max-md:w-screen md:max-h-fit md:flex-1/2 md:flex-row md:justify-end md:text-xs z-10 ${closed ? 'max-md:hidden' : ''} `}
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
        <Link onClick={() => setClosed(true)} to="/catalog">
          catalog
        </Link>
        <hr className="text-zinc-600" />
        <Link onClick={() => setClosed(true)} to="/register">
          register
        </Link>
        <hr className="text-zinc-600" />
        <Link onClick={() => setClosed(true)} to="/login">
          login
        </Link>
      </ul>
    </nav>
  );
}
