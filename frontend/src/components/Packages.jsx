import { Outlet, Link } from 'react-router-dom';

export default function Packages() {
  return (
    <div>
      <h1>Our Packages</h1>
      <nav>
        <Link to="basic">Basic</Link>
        <Link to="premium">Premium</Link>
        <Link to="ultra">Ultra</Link>
        <Link to="elite">Elite</Link>
      </nav>
      <Outlet />
    </div>
  );
}