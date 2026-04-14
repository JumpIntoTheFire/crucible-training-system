import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <section className="not-found">
      <h1>404 – Page Not Found</h1>
      <p>Looks like this page doesn’t exist. Maybe you took a wrong turn at the squat rack?</p>
      <Link to="/" className="back-home">← Back to Home</Link>
    </section>
  );
}