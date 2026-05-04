import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/auth-context';

const API = import.meta.env.VITE_API_URL;

export default function AuthPage() {
  const [tab, setTab] = useState('login');  // 'login' | 'register'
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [status, setStatus] = useState({ type: '', message: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = e =>
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setStatus({ type: '', message: '' });

    try {
      let res, body;

      if (tab === 'register') {
        res = await fetch(`${API}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: form.username,
            email: form.email,
            password: form.password,
          }),
        });
        body = await res.json();
      } else {
        // OAuth2 form-encoded login
        const fd = new URLSearchParams();
        fd.append('username', form.username);
        fd.append('password', form.password);
        res = await fetch(`${API}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: fd.toString(),
        });
        body = await res.json();
      }

      if (!res.ok) {
        setStatus({ type: 'error', message: body.detail || 'Something went wrong.' });
        return;
      }

      login({ token: body.access_token, user_id: body.user_id, username: body.username });
      navigate('/builder');
    } catch {
      setStatus({ type: 'error', message: 'Network error. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-tabs">
          <button
            className={`auth-tab ${tab === 'login' ? 'active' : ''}`}
            onClick={() => { setTab('login'); setStatus({ type: '', message: '' }); }}
          >
            Login
          </button>
          <button
            className={`auth-tab ${tab === 'register' ? 'active' : ''}`}
            onClick={() => { setTab('register'); setStatus({ type: '', message: '' }); }}
          >
            Register
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Username
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder={tab === 'login' ? 'Username or email' : 'Choose a username'}
              required
              autoComplete={tab === 'login' ? 'username' : 'new-username'}
            />
          </label>

          {tab === 'register' && (
            <label>
              Email
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@example.com"
                required
                autoComplete="email"
              />
            </label>
          )}

          <label>
            Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder={tab === 'register' ? 'At least 8 characters' : 'Password'}
              required
              autoComplete={tab === 'login' ? 'current-password' : 'new-password'}
            />
          </label>

          {status.message && (
            <p className={`form-status ${status.type}`}>{status.message}</p>
          )}

          <button type="submit" className="btn-auth-submit" disabled={loading}>
            {loading ? 'Please wait...' : tab === 'login' ? 'Login' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}
