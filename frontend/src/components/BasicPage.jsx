export default function BasicPage() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <h1>Unlock Your Fitness Journey</h1>
        <p className="tagline">
          Start building strength, routine, and results — one rep at a time.
        </p>
      </section>

      {/* Package Highlights */}
      <section className="package-highlights">
        <h2>Beginner Package – £60/month</h2>
        <ul>
          <li>✅ Pre-made exercise programs tailored for new lifters</li>
          <li>👥 Exclusive access to the CTS community</li>
          <li>🥗 Customised meal plan to fuel your goals</li>
        </ul>
      </section>

      {/* Call to Action */}
      <section className="cta">
        <p className="pitch">
          This isn't just a workout plan. It's the foundation of your transformation.
        </p>
        <p className="contact">
          Got questions? Reach out at{" "}
          <a href="mailto:email@example.com">email@example.com</a> or call{" "}
          <a href="tel:07400123456">07400 123456</a>.
        </p>
        <a
          href="https://buy.stripe.com/test_28obJpbTl2us58g001"
          className="btn-submit"
        >
          Subscribe via Stripe →
        </a>
        <p className="disclaimer">
          Subscription billed monthly. Cancel anytime.
        </p>
      </section>
    </>
  );
}