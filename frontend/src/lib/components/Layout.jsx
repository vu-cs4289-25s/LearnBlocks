import Nav from './Navbar';

export default function Layout({ children }){
  return (
    
    <div className="flex min-h-screen flex-col dark:bg-zinc-800 dark:text-zinc-100">
      <Nav />
      {children}
    </div>
  );
}

