import { useState, useEffect, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ExerciseCard from './ExerciseCard';
import WorkoutPanel from './WorkoutPanel';
import { useAuth } from '../contexts/AuthContext';

const API = import.meta.env.VITE_API_URL;
const LIMIT = 20;

const MUSCLES = [
  'abdominals', 'abductors', 'adductors', 'biceps', 'calves',
  'chest', 'forearms', 'glutes', 'hamstrings', 'lats',
  'lower back', 'middle back', 'neck', 'quadriceps',
  'shoulders', 'traps', 'triceps',
];

const CATEGORIES = [
  'cardio',
  'olympic weightlifting',
  'plyometrics',
  'powerlifting',
  'strength',
  'stretching',
  'strongman',
];

function loadLocalWorkouts() {
  try { return JSON.parse(localStorage.getItem('cts_workouts') || '[]'); }
  catch { return []; }
}

export default function ExerciseBuilder() {
  const { auth } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const [exercises, setExercises]   = useState([]);
  const [search, setSearch]         = useState('');
  const [muscle, setMuscle]         = useState('');
  const [category, setCategory]     = useState('');
  const [skip, setSkip]             = useState(0);
  const [hasMore, setHasMore]       = useState(true);
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState(null);

  const [workout, setWorkout]             = useState([]);
  const [workoutName, setWorkoutName]     = useState('');
  const [savedWorkouts, setSavedWorkouts] = useState([]);
  const [saveError, setSaveError]         = useState(null);

  // ── Load saved workouts ────────────────────────────────────────────────────

  const fetchSavedWorkouts = useCallback(async () => {
    if (!auth) {
      setSavedWorkouts(loadLocalWorkouts());
      return;
    }
    try {
      const res = await fetch(`${API}/workouts`, {
        headers: { Authorization: `Bearer ${auth.token}` },
      });
      if (res.ok) {
        setSavedWorkouts(await res.json());
      }
    } catch {
      // silently fall back to empty
    }
  }, [auth]);

  useEffect(() => { fetchSavedWorkouts(); }, [fetchSavedWorkouts]);

  // ── Load handoff: if /history navigated here with state.plan, populate the
  //    builder with that plan and clear the navigation state so a subsequent
  //    refresh doesn't re-load it.
  useEffect(() => {
    const planFromState = location.state?.plan;
    if (planFromState) {
      setWorkout(planFromState.exercises || []);
      setWorkoutName(planFromState.name || '');
      navigate(location.pathname, { replace: true, state: null });
    }
  }, [location.state, location.pathname, navigate]);

  // ── Fetch exercises ────────────────────────────────────────────────────────

  const fetchExercises = useCallback(async (q, m, cat, s) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ skip: s, limit: LIMIT });
      if (q) params.append('search', q);
      if (m) params.append('muscle', m);
      if (cat) params.append('category', cat);
      const res = await fetch(`${API}/exercises?${params}`);
      if (!res.ok) throw new Error('Failed to load exercises');
      const data = await res.json();
      setExercises(prev => s === 0 ? data : [...prev, ...data]);
      setHasMore(data.length === LIMIT);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounce search/muscle/category — reset to page 0 on filter change
  useEffect(() => {
    const timer = setTimeout(() => {
      setSkip(0);
      fetchExercises(search, muscle, category, 0);
    }, 300);
    return () => clearTimeout(timer);
  }, [search, muscle, category, fetchExercises]);

  const loadMore = () => {
    const next = skip + LIMIT;
    setSkip(next);
    fetchExercises(search, muscle, category, next);
  };

  // ── Workout actions ────────────────────────────────────────────────────────

  const addToWorkout = (exercise) =>
    setWorkout(prev => [...prev, { exercise, sets: 3, reps: 10, rest: 60 }]);

  const updateEntry = (index, field, value) =>
    setWorkout(prev => prev.map((e, i) => i === index ? { ...e, [field]: value } : e));

  const removeEntry = (index) =>
    setWorkout(prev => prev.filter((_, i) => i !== index));

  const moveEntry = (index, dir) =>
    setWorkout(prev => {
      const next = [...prev];
      const swap = index + dir;
      if (swap < 0 || swap >= next.length) return prev;
      [next[index], next[swap]] = [next[swap], next[index]];
      return next;
    });

  // Slim exercise to display-only fields before persisting
  const slimExercise = (e) => ({
    id: e.exercise.id,
    name: e.exercise.name,
    category: e.exercise.category,
    level: e.exercise.level,
    primaryMuscles: e.exercise.primaryMuscles,
    startImage: e.exercise.startImage,
  });

  const saveWorkout = async () => {
    if (!workoutName.trim() || workout.length === 0) return;
    setSaveError(null);

    const exercises = workout.map(e => ({
      sets: e.sets,
      reps: e.reps,
      rest: e.rest,
      exercise: slimExercise(e),
    }));

    if (auth) {
      // Save to database
      try {
        const res = await fetch(`${API}/workouts`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${auth.token}`,
          },
          body: JSON.stringify({ name: workoutName.trim(), exercises }),
        });
        if (!res.ok) throw new Error('Failed to save');
        await fetchSavedWorkouts();
      } catch (e) {
        setSaveError('Could not save to account. Try again.');
      }
    } else {
      // Fallback: localStorage
      try {
        const plan = {
          id: Date.now(),
          name: workoutName.trim(),
          exercises,
          created_at: new Date().toISOString(),
        };
        const updated = [plan, ...savedWorkouts.filter(w => w.name !== plan.name)];
        localStorage.setItem('cts_workouts', JSON.stringify(updated));
        setSavedWorkouts(updated);
      } catch (e) {
        console.error('Failed to save workout:', e);
      }
    }
  };

  const loadWorkout = (plan) => {
    setWorkout(plan.exercises);
    setWorkoutName(plan.name);
  };

  const deleteWorkout = async (id) => {
    if (auth) {
      try {
        await fetch(`${API}/workouts/${id}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${auth.token}` },
        });
        await fetchSavedWorkouts();
      } catch {
        // silently ignore
      }
    } else {
      const updated = savedWorkouts.filter(w => w.id !== id);
      setSavedWorkouts(updated);
      localStorage.setItem('cts_workouts', JSON.stringify(updated));
    }
  };

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="builder-layout">

      {/* Left: Exercise Library */}
      <section className="exercise-library">
        <h1>Exercise Library</h1>

        <div className="library-filters">
          <input
            type="text"
            className="search-input"
            placeholder="Search exercises..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <select
            className="muscle-select"
            value={muscle}
            onChange={e => setMuscle(e.target.value)}
          >
            <option value="">All muscles</option>
            {MUSCLES.map(m => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>

          <select
            className="muscle-select"
            value={category}
            onChange={e => setCategory(e.target.value)}
          >
            <option value="">All types</option>
            {CATEGORIES.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {error && <p className="builder-error">{error}</p>}

        <div className="exercise-grid">
          {exercises.map(ex => (
            <ExerciseCard key={ex.id} exercise={ex} onAdd={addToWorkout} />
          ))}
        </div>

        {!loading && exercises.length === 0 && !error && (
          <p className="builder-empty">No exercises found.</p>
        )}
        {loading && <p className="builder-loading">Loading...</p>}
        {!loading && hasMore && (
          <button className="btn-load-more" onClick={loadMore}>Load more</button>
        )}
      </section>

      {/* Right: Workout Panel */}
      <WorkoutPanel
        workout={workout}
        workoutName={workoutName}
        savedWorkouts={savedWorkouts}
        isLoggedIn={!!auth}
        saveError={saveError}
        onWorkoutNameChange={setWorkoutName}
        onUpdate={updateEntry}
        onRemove={removeEntry}
        onMove={moveEntry}
        onSave={saveWorkout}
        onLoad={loadWorkout}
        onDelete={deleteWorkout}
        onClear={() => setWorkout([])}
      />
    </div>
  );
}
