import Nav from './Navbar';

const role = 's'

const allNavs = {
  login: '/login',
  register: '/register',
  catalog: '/catalog',
  playground: '/playground',
  home: `/${role}/home`,
  courses: `/${role}/courses`,
}

export default function Layout({ children }) {
  return (
    <main className="flex min-h-screen flex-col dark:bg-zinc-900 dark:text-zinc-100">
      <Nav />
      {children}
    </main>
  );
}
