import { useState,useEffect } from "react";
import ErrorBar from "./ErrorBar";
import Navbar from "./Navbar";
import { AuthUserContext, ErrorContext } from "$lib/contexts/ErrorContext";

export default function Layout({ children }) {
  const [error, setError] = useState(null);
  const [authUser, setAuthUser] = useState(() => {
    try {
      const storedUser = localStorage.getItem("authUser");
      return storedUser ? JSON.parse(storedUser) : null;
    } catch (e) {
      console.error("Error loading authUser from localStorage:", e);
      return null;
    }
  });

  useEffect(() => {
    try {
      if (authUser) {
        localStorage.setItem("authUser", JSON.stringify(authUser));
      } else {
        // Clear stored authUser when authUser state is set to null.
        localStorage.removeItem("authUser");
      }
    } catch (e) {
      console.error("Error saving authUser to localStorage:", e);
    }
  }, [authUser]);

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
