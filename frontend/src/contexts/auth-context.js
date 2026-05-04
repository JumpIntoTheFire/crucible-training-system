// Non-component module — holds the AuthContext constant and the useAuth hook.
// Lives separately from AuthContext.jsx so that file can export only the
// AuthProvider component (satisfies react-refresh/only-export-components).
import { createContext, useContext } from 'react';

export const AuthContext = createContext(null);

export function useAuth() {
  return useContext(AuthContext);
}
