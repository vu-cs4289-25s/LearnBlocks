import { useContext } from "react";
import { ErrorContext } from "$lib/contexts/Context";
import { Button } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";

/**
 * @param {object} param0 : Props for the Navbar
 * @param {import('$lib/types/common.mjs').NavLinkType[]} param0.navLinkData : Navbar link data to populate links
 * @returns {import('react').ReactElement} The navbar element
 */
export default function ErrorBar() {
  const { error, setError } = useContext(ErrorContext);

  return (
    <section
      className={`flex flex-row justify-between bg-red-800 px-2 ${error ? "h-fit py-1" : "h-0"}`}
    >
    <div/>
      <h1 className="text-lg font-bold ">{error}</h1>
      <Button onClick={() => setError("")} >
        <XMarkIcon
          className={`h-8 cursor-pointer ${error ? "" : "hidden"}`}
          alt="Close Error"
        />
      </Button>
    </section>
  );
}
