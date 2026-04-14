import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function WorkoutPanel({
  workout,
  workoutName,
  savedWorkouts,
  isLoggedIn,
  saveError,
  onWorkoutNameChange,
  onUpdate,
  onRemove,
  onMove,
  onSave,
  onLoad,
  onDelete,
  onClear,
}) {
  const [saveMsg, setSaveMsg] = useState('');

  const handleSave = async () => {
    await onSave();
    if (!saveError) {
      setSaveMsg('Saved!');
      setTimeout(() => setSaveMsg(''), 2000);
    }
  };

  return (
    <aside className="workout-panel">
      <h2>My Workout</h2>

      {workout.length === 0 ? (
        <p className="panel-empty">
          Add exercises from the library to build your workout.
        </p>
      ) : (
        <>
          <ul className="workout-list">
            {workout.map((entry, i) => (
              <li key={i} className="workout-entry">
                <div className="entry-header">
                  <span className="entry-name">{entry.exercise.name}</span>
                  <div className="entry-controls">
                    <button
                      className="btn-reorder"
                      onClick={() => onMove(i, -1)}
                      disabled={i === 0}
                      aria-label="Move up"
                    >↑</button>
                    <button
                      className="btn-reorder"
                      onClick={() => onMove(i, 1)}
                      disabled={i === workout.length - 1}
                      aria-label="Move down"
                    >↓</button>
                    <button
                      className="btn-remove"
                      onClick={() => onRemove(i)}
                      aria-label="Remove"
                    >✕</button>
                  </div>
                </div>

                <div className="entry-inputs">
                  <label>
                    Sets
                    <input
                      type="number"
                      min="1"
                      value={entry.sets}
                      onChange={e => onUpdate(i, 'sets', Number(e.target.value))}
                    />
                  </label>
                  <label>
                    Reps
                    <input
                      type="number"
                      min="1"
                      value={entry.reps}
                      onChange={e => onUpdate(i, 'reps', Number(e.target.value))}
                    />
                  </label>
                  <label>
                    Rest (s)
                    <input
                      type="number"
                      min="0"
                      step="15"
                      value={entry.rest}
                      onChange={e => onUpdate(i, 'rest', Number(e.target.value))}
                    />
                  </label>
                </div>
              </li>
            ))}
          </ul>

          <button className="btn-clear" onClick={onClear}>
            Clear all
          </button>
        </>
      )}

      <div className="save-section">
        <input
          type="text"
          className="workout-name-input"
          placeholder="Name your workout..."
          value={workoutName}
          onChange={e => onWorkoutNameChange(e.target.value)}
        />
        <button
          className="btn-save"
          onClick={handleSave}
          disabled={!workoutName.trim() || workout.length === 0}
        >
          Save Workout
        </button>
        {saveMsg && <p className="save-confirm">{saveMsg}</p>}
        {saveError && <p className="form-status error">{saveError}</p>}
        {!isLoggedIn && (
          <p className="save-hint">
            <Link to="/auth">Log in</Link> to save workouts to your account.
          </p>
        )}
      </div>

      {savedWorkouts.length > 0 && (
        <div className="saved-workouts">
          <h3>Saved Workouts</h3>
          <ul className="saved-list">
            {savedWorkouts.map(plan => (
              <li key={plan.id} className="saved-plan">
                <span className="saved-name">{plan.name}</span>
                <div className="saved-actions">
                  <button className="btn-load" onClick={() => onLoad(plan)}>Load</button>
                  <button className="btn-delete" onClick={() => onDelete(plan.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </aside>
  );
}
