import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <>
      <header>
        <div className="image-grid">
          <img className="above" src="/images/above.png" alt="Top left image" />
          <img className="the-one" src="/images/the-one.png" alt="Centered middle image" />
          <img className="below" src="/images/below.png" alt="Bottom right image" />
        </div>

        <div className="hero-cta">
          <Link to="/builder" className="btn-hero">
            Build Your Workout →
          </Link>
        </div>
      </header>

      <section aria-labelledby="about-cts">
        <h2 id="about-cts">What Is CTS?</h2>
        <p>
          This is a training system designed to help you improve your mindset.<br />
          Which in turn develops both your body and mind.<br />
          So that you can better serve yourself—and others.
        </p>
        <p>At CTS, we pride ourselves on 3 core pillars that guide everything we do:</p>
      </section>

      <section aria-labelledby="pillars">
        <h2 id="pillars">Our Pillars</h2>
        <div className="pillar-container">
          <img className="pillar" src="/images/service.png" alt="Pillar of Service" />
          <img className="pillar" src="/images/accountability.png" alt="Pillar of Accountability" />
          <img className="pillar" src="/images/hardwork.png" alt="Pillar of Hard Work" />
        </div>
      </section>
    </>
  );
}
