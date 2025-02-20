import Nav from './Navbar';

export default function Layout({ children }){
  return (
    <div className="flex min-h-screen flex-col dark:bg-gray-800 dark:text-gray-100">
      <Nav />
      {children}
    </div>
  );
}

