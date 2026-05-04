import { useState, useCallback } from 'react';
import { AuthContext } from './auth-context';

function loadStoredAuth() {
  try {
    const raw = localStorage.getItem('cts_auth');
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(loadStoredAuth);  // { token, user_id, username }

  const login = useCallback((tokenData) => {
    localStorage.setItem('cts_auth', JSON.stringify(tokenData));
    setAuth(tokenData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('cts_auth');
    setAuth(null);
  }, []);

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
