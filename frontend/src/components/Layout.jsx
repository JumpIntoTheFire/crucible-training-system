import { useState } from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/auth-context';

export default function Layout() {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const closeMenu = () => setMenuOpen(false);

  const handleLogout = () => {
    closeMenu();
    logout();
    navigate('/');
  };

  return (
    <div>
      <nav>
        <button
          className="nav-toggle"
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((o) => !o)}
        >
          ☰
        </button>
        <ul className={`nav-list ${menuOpen ? 'nav-list--open' : ''}`}>
          <li><Link to="/" onClick={closeMenu}><strong>Home</strong></Link></li>

          <li className="dropdown">
            <Link to="/packages" onClick={closeMenu}><strong>Packages</strong></Link>
            <ul className="dropdown-menu">
              <li><Link to="/packages/basic" onClick={closeMenu}><strong>Basic</strong></Link></li>
              <li><Link to="/packages/premium" onClick={closeMenu}><strong>Premium</strong></Link></li>
              <li><Link to="/packages/ultra" onClick={closeMenu}><strong>Ultra</strong></Link></li>
              <li><Link to="/packages/elite" onClick={closeMenu}><strong>Elite</strong></Link></li>
            </ul>
          </li>

          <li><Link to="/builder" onClick={closeMenu}><strong>Builder</strong></Link></li>
          {auth && (
            <li><Link to="/history" onClick={closeMenu}><strong>History</strong></Link></li>
          )}
          <li><Link to="/contact" onClick={closeMenu}><strong>Contact</strong></Link></li>

          <li className="nav-auth">
            {auth ? (
              <>
                <span className="nav-username">{auth.username}</span>
                <button className="btn-nav-logout" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <Link to="/auth" className="btn-nav-login" onClick={closeMenu}>Login</Link>
            )}
          </li>
        </ul>
      </nav>
      <Outlet />
    </div>
  );
}
