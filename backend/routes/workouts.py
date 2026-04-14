from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any

from backend.models import WorkoutPlan, User, get_db
from backend.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class WorkoutPlanIn(BaseModel):
    name: str
    exercises: list[Any]  # list of exercise entry objects from the frontend


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

@router.get("", response_model=list[WorkoutPlanOut])
def list_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plans = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )
    return [WorkoutPlanOut.from_orm_model(p) for p in plans]


@router.post("", response_model=WorkoutPlanOut, status_code=201)
def create_workout(
    payload: WorkoutPlanIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = WorkoutPlan(
        user_id=current_user.id,
        name=payload.name,
        exercises=payload.exercises,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return WorkoutPlanOut.from_orm_model(plan)


@router.delete("/{plan_id}", status_code=204)
def delete_workout(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id,
        WorkoutPlan.user_id == current_user.id,
    ).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    db.delete(plan)
    db.commit()
