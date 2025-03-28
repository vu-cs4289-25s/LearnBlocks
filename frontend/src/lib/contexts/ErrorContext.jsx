import { createContext } from "react";

export const ErrorContext = createContext({ error: null, setError: null });
export const AuthUserContext = createContext({ authUser: null, setAuthUser: null });
