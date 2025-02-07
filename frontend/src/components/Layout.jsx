import Nav from './Navbar';

export default function Layout({ children }){
  return (
    <div className="flex min-h-screen flex-col dark:bg-gray-800">
      <Nav />
      {children}
    </div>
  );
}

