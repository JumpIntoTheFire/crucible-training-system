import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.models import Exercise, get_db
from backend.schemas.exercises import ExerciseSchema

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Exercises"])

VALID_CATEGORIES = frozenset([
    "cardio",
    "olympic weightlifting",
    "plyometrics",
    "powerlifting",
    "strength",
    "stretching",
    "strongman",
])

VALID_MUSCLES = frozenset([
    "abdominals", "abductors", "adductors", "biceps", "calves",
    "chest", "forearms", "glutes", "hamstrings", "lats",
    "lower back", "middle back", "neck", "quadriceps",
    "shoulders", "traps", "triceps",
])


@router.get(
    "/exercises",
    response_model=List[ExerciseSchema],
    summary="List exercises",
    description=(
        "Retrieve exercises from the library. "
        "Supports filtering by name, muscle group, and training category, with pagination."
    ),
)
def get_exercises(
    search: Optional[str] = Query(None, description="Filter by exercise name (case-insensitive)"),
    muscle: Optional[str] = Query(None, description="Filter by primary or secondary muscle"),
    category: Optional[str] = Query(None, description="Filter by training category"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results to return"),
    db: Session = Depends(get_db),
):
    if muscle and muscle not in VALID_MUSCLES:
        raise HTTPException(status_code=400, detail=f"Invalid muscle '{muscle}'. Valid options: {sorted(VALID_MUSCLES)}")

    if category and category not in VALID_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category '{category}'. Valid options: {sorted(VALID_CATEGORIES)}")

    query = db.query(Exercise)

    if search:
        query = query.filter(Exercise.name.ilike(f"%{search}%"))

    if muscle:
        query = query.filter(
            Exercise.primaryMuscles.any(muscle) |
            Exercise.secondaryMuscles.any(muscle)
        )

    if category:
        query = query.filter(Exercise.category == category)

    return query.offset(skip).limit(limit).all()
