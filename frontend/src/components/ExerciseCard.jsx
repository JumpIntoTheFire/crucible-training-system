export default function ExerciseCard({ exercise, onAdd }) {
  const imgSrc = exercise.startImage
    ? `${import.meta.env.VITE_API_URL}${exercise.startImage}`
    : null;

  return (
    <div className="exercise-card">
      {imgSrc && (
        <img src={imgSrc} alt={exercise.name} className="card-image" />
      )}
      <div className="card-body">
        <h3 className="card-name">{exercise.name}</h3>
        <div className="card-badges">
          {exercise.category && <span className="badge">{exercise.category}</span>}
          {exercise.level && <span className="badge badge-level">{exercise.level}</span>}
        </div>
        {exercise.primaryMuscles?.length > 0 && (
          <p className="card-muscles">{exercise.primaryMuscles.join(', ')}</p>
        )}
        <button className="btn-add" onClick={() => onAdd(exercise)}>
          + Add to Workout
        </button>
      </div>
    </div>
  );
}
