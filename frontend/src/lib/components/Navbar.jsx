import { Link } from 'react-router-dom';


export default function Nav() {
  return (
    <div className="dark:bg-gray-800">
      <div href={import.meta.env.BASE_URL}>
        <img
          src="/learnblocks.svg"
          className="mr-3 h-6 sm:h-9"
          alt="Learn Blocks Logo"
        />
        <span className="text-xl self-center font-semibold">
          LearnBlocks
        </span>
      </div>
      <div />
      <div>
        <div href="/register"> Register </div>
        <div href="/login">Login</div>
      </div>
    </div >
  );
}
