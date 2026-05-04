import { useState, useEffect } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const API = import.meta.env.VITE_API_URL;

export default function WorkoutHistory() {
  const { auth } = useAuth();
  const navigate = useNavigate();

  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    if (!auth) return;
    const fetchPlans = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API}/workouts`, {
          headers: { Authorization: `Bearer ${auth.token}` },
        });
        if (!res.ok) throw new Error('Could not load workouts');
        const data = await res.json();
        setPlans(data); // server returns newest-first
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPlans();
  }, [auth]);

  // Auth-required: redirect to /auth if logged out
  if (!auth) return <Navigate to="/auth" replace />;

  const formatDate = (iso) => {
    if (!iso) return 'Unknown date';
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return 'Unknown date';
    return d.toLocaleDateString('en-GB', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const handleLoad = (plan) => {
    navigate('/builder', { state: { plan } });
  };

  const handleDelete = async (id) => {
    setDeletingId(id);
    setError(null);
    try {
      const res = await fetch(`${API}/workouts/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${auth.token}` },
      });
      if (!res.ok && res.status !== 204) throw new Error('Could not delete workout');
      setPlans((prev) => prev.filter((p) => p.id !== id));
    } catch (e) {
      setError(e.message);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <section className="history-page">
      <header className="history-header">
        <h1>Workout History</h1>
        <p className="history-subtitle">All your saved workouts, most recent first.</p>
      </header>

      {error && <p className="history-error">{error}</p>}

      {loading ? (
        <p className="history-loading">Loading workouts…</p>
      ) : plans.length === 0 ? (
        <div className="history-empty">
          <p>You haven&apos;t saved any workouts yet.</p>
          <Link to="/builder" className="btn-hero">Build Your First Workout →</Link>
        </div>
      ) : (
        <ul className="history-list">
          {plans.map((plan) => {
            const exerciseCount = Array.isArray(plan.exercises) ? plan.exercises.length : 0;
            return (
              <li key={plan.id} className="history-card">
                <div className="history-card-info">
                  <h2 className="history-card-name">{plan.name}</h2>
                  <p className="history-card-meta">
                    {formatDate(plan.created_at)}
                    {' · '}
                    {exerciseCount} {exerciseCount === 1 ? 'exercise' : 'exercises'}
                  </p>
                </div>
                <div className="history-card-actions">
                  <button
                    className="btn-load"
                    onClick={() => handleLoad(plan)}
                    aria-label={`Load ${plan.name} into the builder`}
                  >
                    Load in Builder
                  </button>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(plan.id)}
                    disabled={deletingId === plan.id}
                    aria-label={`Delete ${plan.name}`}
                  >
                    {deletingId === plan.id ? 'Deleting…' : 'Delete'}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
