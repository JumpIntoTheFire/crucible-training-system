export default function UltraPage() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <h1>Ultra Tier</h1>
        <p className="tagline">
          Bespoke strategy for performance, recovery, and refined movement.
        </p>
      </section>

      {/* Package Highlights */}
      <section className="package-highlights">
        <h2>£120/month</h2>
        <ul>
          <li>🧠 Bespoke exercise programming with advanced movement analysis</li>
          <li>🥗 Customised nutrition plan tailored to your physiology</li>
          <li>📂 Full access to pre-built CTS programs</li>
          <li>👥 Ongoing membership in CTS community</li>
        </ul>
      </section>

      {/* Call to Action */}
      <section className="cta">
        <p className="pitch">
          For those who want precision over guesswork. Ultra is strategy-first
          coaching, not templated plans.
        </p>
        <p className="contact">
          Let’s talk:{" "}
          <a href="mailto:email@example.com">email@example.com</a> or{" "}
          <a href="tel:07400123456">07400 123456</a>
        </p>
        <a
          href="https://buy.stripe.com/test_cN26s92Wxge7gKA001"
          className="btn-submit"
        >
          Join Ultra Tier →
        </a>
        <p className="disclaimer">
          No commitment. Cancel anytime. Secure checkout via Stripe.
        </p>
      </section>
    </>
  );
}