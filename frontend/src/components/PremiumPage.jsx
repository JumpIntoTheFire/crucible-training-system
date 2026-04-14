export default function PremiumPage() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <h1>Premium Tier</h1>
        <p className="tagline">
          Structure without stress. Enjoy personalised programming, nutrition,
          and lifestyle support.
        </p>
      </section>

      {/* Package Highlights */}
      <section className="package-highlights">
        <h2>£90/month</h2>
        <ul>
          <li>📋 Bespoke exercise program with structured progression</li>
          <li>🥗 Personalised meal plan and nutrition coaching</li>
          <li>📂 Access to curated CTS workouts</li>
          <li>👥 Community access — support, check-ins &amp; shared wins</li>
        </ul>
      </section>

      {/* Call to Action */}
      <section className="cta">
        <p className="pitch">
          Premium delivers purpose without overwhelm. Ideal for those building
          momentum and mastering consistency.
        </p>
        <p className="contact">
          Need clarity? Contact us at{" "}
          <a href="mailto:email@example.com">email@example.com</a> or call{" "}
          <a href="tel:07400123456">07400 123456</a>
        </p>
        <a
          href="https://buy.stripe.com/test_eVa7uN0Wxge7fAAeUU"
          className="btn-submit"
        >
          Join Premium Tier →
        </a>
        <p className="disclaimer">
          Monthly billing. Cancel anytime. Secure Stripe checkout.
        </p>
      </section>
    </>
  );
}