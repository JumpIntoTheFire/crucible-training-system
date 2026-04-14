from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.models import Exercise, get_db
from backend.schemas.exercises import ExerciseSchema

router = APIRouter()

CATEGORIES = [
    "cardio",
    "olympic weightlifting",
    "plyometrics",
    "powerlifting",
    "strength",
    "stretching",
    "strongman",
]


@router.get("/exercises", response_model=List[ExerciseSchema])
def get_exercises(
    search: Optional[str] = Query(None, description="Filter by exercise name"),
    muscle: Optional[str] = Query(None, description="Filter by primary or secondary muscle"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Results to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
    db: Session = Depends(get_db),
):
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
