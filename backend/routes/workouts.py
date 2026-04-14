import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Any

from backend.models import WorkoutPlan, User, get_db
from backend.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workouts", tags=["Workouts"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class WorkoutEntryExercise(BaseModel):
    id: int
    name: str
    category: str | None = None
    level: str | None = None
    primaryMuscles: list[str] = []
    startImage: str | None = None


class WorkoutEntry(BaseModel):
    sets: int = Field(ge=1, le=100)
    reps: int = Field(ge=1, le=100)
    rest: int = Field(ge=0, le=3600)
    exercise: WorkoutEntryExercise


class WorkoutPlanIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    exercises: list[WorkoutEntry]


class WorkoutPlanOut(BaseModel):
    id: int
    name: str
    exercises: list[Any]
    created_at: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, plan: WorkoutPlan) -> "WorkoutPlanOut":
        return cls(
            id=plan.id,
            name=plan.name,
            exercises=plan.exercises or [],
            created_at=plan.created_at.isoformat(),
        )


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("", response_model=list[WorkoutPlanOut], summary="List user's workout plans")
def list_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all saved workout plans for the authenticated user, newest first."""
    plans = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )
    return [WorkoutPlanOut.from_orm_model(p) for p in plans]


@router.post("", response_model=WorkoutPlanOut, status_code=201, summary="Save a workout plan")
def create_workout(
    payload: WorkoutPlanIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save a named workout plan (list of exercises with sets/reps/rest) for the authenticated user."""
    plan = WorkoutPlan(
        user_id=current_user.id,
        name=payload.name,
        exercises=[e.model_dump() for e in payload.exercises],
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    logger.info("Workout plan saved (user_id=%s, plan_id=%s)", current_user.id, plan.id)
    return WorkoutPlanOut.from_orm_model(plan)


@router.delete("/{plan_id}", status_code=204, summary="Delete a workout plan")
def delete_workout(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a workout plan. Returns 404 if the plan does not belong to the authenticated user."""
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == current_user.id,
    ).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    db.delete(plan)
    db.commit()
    logger.info("Workout plan deleted (user_id=%s, plan_id=%s)", current_user.id, plan_id)
