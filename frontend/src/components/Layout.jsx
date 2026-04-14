import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Layout() {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div>
      <nav>
        <ul className="nav-list">
          <li><Link to="/"><strong>Home</strong></Link></li>

          <li className="dropdown">
            <Link to="/packages"><strong>Packages</strong></Link>
            <ul className="dropdown-menu">
              <li><Link to="/packages/basic"><strong>Basic</strong></Link></li>
              <li><Link to="/packages/premium"><strong>Premium</strong></Link></li>
              <li><Link to="/packages/ultra"><strong>Ultra</strong></Link></li>
              <li><Link to="/packages/elite"><strong>Elite</strong></Link></li>
            </ul>
          </li>

          <li><Link to="/builder"><strong>Builder</strong></Link></li>
          <li><Link to="/contact"><strong>Contact</strong></Link></li>

          <li className="nav-auth">
            {auth ? (
              <>
                <span className="nav-username">{auth.username}</span>
                <button className="btn-nav-logout" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <Link to="/auth" className="btn-nav-login">Login</Link>
            )}
          </li>
        </ul>
      </nav>
      <Outlet />
    </div>
  );
}
