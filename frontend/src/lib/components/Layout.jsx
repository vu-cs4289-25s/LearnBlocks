import { useState } from "react";
import ErrorBar from "./ErrorBar";
import Navbar from "./Navbar";
import { AuthUserContext, ErrorContext } from "$lib/contexts/ErrorContext";

export default function Layout({ children }) {
  const [error, setError] = useState(null);
  const [authUser, setAuthUser] = useState(null);
  return (
    <main className="flex min-h-screen flex-col dark:bg-zinc-900 dark:text-zinc-100">
      <ErrorContext.Provider value={{ error, setError }}>
        <AuthUserContext.Provider value={{ authUser, setAuthUser }}>
          <Navbar />
          <ErrorBar />
          {children}
        </AuthUserContext.Provider>
      </ErrorContext.Provider>
    </main>
  );
}
