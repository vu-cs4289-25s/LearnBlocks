import Nav from './Navbar';

export default function Layout({ children }: LayoutProps): JSX.Element {
  return (
    <div className="flex min-h-screen flex-col dark:bg-gray-800">
      <Nav />
      {children}
    </div>
  );
}

interface LayoutProps {
  children: JSX.Element;
}
