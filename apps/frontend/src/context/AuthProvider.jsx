import { useCallback, useMemo, useState } from "react";

import { clearStoredAuth, getStoredAuth, setStoredAuth } from "../auth/storage";
import { AuthContext } from "./auth-context";

export default function AuthProvider({ children }) {
  const [auth, setAuth] = useState(() => getStoredAuth());

  const login = useCallback((payload) => {
    setStoredAuth(payload);
    setAuth(payload);
  }, []);

  const logout = useCallback(() => {
    clearStoredAuth();
    setAuth(null);
  }, []);

  const value = useMemo(
    () => ({
      auth,
      isAuthenticated: Boolean(auth?.access_token),
      user: auth?.user ?? null,
      login,
      logout,
    }),
    [auth, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
