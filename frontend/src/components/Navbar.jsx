import { Link } from 'react-router-dom';

import {
  Navbar,
  NavbarBrand,
  NavbarToggle,
  NavbarCollapse,
  NavbarLink,
} from 'flowbite-react';

export default function Nav() {
  return (
    <Navbar fluid className="dark:bg-nb-gray-400">
      <NavbarBrand as={Link} href={import.meta.env.BASE_URL}>
        <img
          src="learnblocks.svg"
          className="mr-3 h-6 sm:h-9"
          alt="Learn Blocks Logo"
        />
        <span className="text-xl self-center whitespace-nowrap font-semibold dark:text-white">
          LearnBlocks
        </span>
      </NavbarBrand>
      <NavbarToggle />
      <NavbarCollapse>
        <NavbarLink href="##">Register</NavbarLink>
        <NavbarLink href="#">Login</NavbarLink>
      </NavbarCollapse>
    </Navbar>
  );
}
