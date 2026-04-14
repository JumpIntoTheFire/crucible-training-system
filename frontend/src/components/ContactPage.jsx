import { useState, useRef } from 'react';

export default function ContactPage() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState(null);
  const [statusType, setStatusType] = useState('');
  const [loading, setLoading] = useState(false);
  const controllerRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    setLoading(true);

    controllerRef.current = new AbortController();
    const timeout = setTimeout(() => controllerRef.current.abort(), 10000);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
        signal: controllerRef.current.signal,
      });

      clearTimeout(timeout);

      if (res.ok) {
        setStatus('Thanks — your message has been sent.');
        setStatusType('success');
        setFormData({ name: '', email: '', message: '' });
      } else {
        const err = await res.json().catch(() => ({}));
        setStatus(err?.detail || `Request failed (${res.status})`);
        setStatusType('error');
      }
    } catch (err) {
      clearTimeout(timeout);
      setStatus('Network error. Please try again.');
      setStatusType('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="contact">
      <h1>Contact Us</h1>
      <form className="contact-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Your Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            name="message"
            rows="6"
            value={formData.message}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send Message →'}
        </button>

        {status && (
          <p className={`form-status ${statusType}`} aria-live="polite">
            {status}
          </p>
        )}
      </form>
    </section>
  );
}
