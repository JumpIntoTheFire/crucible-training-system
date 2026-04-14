export default function ElitePage() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <h1>Elite Tier</h1>
        <p className="tagline">
          Precision coaching, tailored analysis, and high-touch guidance for
          peak performance.
        </p>
      </section>

      {/* Package Highlights */}
      <section className="package-highlights">
        <h2>£150/month</h2>
        <ul>
          <li>🎥 45-minute bi-weekly video call</li>
          <li>📋 Bespoke exercise program with full movement analysis</li>
          <li>🥗 Customised meal plan with advanced breakdown</li>
          <li>📁 Access to CTS community + complete program archive</li>
        </ul>
      </section>

      {/* Call to Action */}
      <section className="cta">
        <p className="pitch">
          Elite is for those chasing mastery — strategic, personal, and
          outcome-driven. This is where coaching becomes craft.
        </p>
        <p className="contact">
          Let’s connect:{" "}
          <a href="mailto:email@example.com">email@example.com</a> or call{" "}
          <a href="tel:07400123456">07400 123456</a>
        </p>
        <a
          href="https://buy.stripe.com/test_XYZEliteTier123"
          className="btn-submit"
        >
          Apply for Elite Tier →
        </a>
        <p className="disclaimer">
          Membership billed monthly. Cancel anytime. Secure Stripe checkout.
        </p>
      </section>
    </>
  );
}