import { Outlet, Link } from 'react-router-dom';

export default function Packages() {
  return (
    <div className="packages-page">
      <h1 className="packages-title">Our Packages</h1>
      <p className="packages-subtitle">Pick the tier that fits where you are right now.</p>
      <nav className="tier-nav" aria-label="Package tiers">
        <Link to="basic" className="tier-link">Basic</Link>
        <Link to="premium" className="tier-link">Premium</Link>
        <Link to="ultra" className="tier-link">Ultra</Link>
        <Link to="elite" className="tier-link">Elite</Link>
      </nav>
      <Outlet />
    </div>
  );
}