from pydantic import BaseModel
from typing import Optional, List


class ExerciseSchema(BaseModel):
    id: int
    name: str
    force: Optional[str] = None
    level: Optional[str] = None
    mechanic: Optional[str] = None
    equipment: Optional[str] = None
    primaryMuscles: Optional[List[str]] = None
    secondaryMuscles: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    category: Optional[str] = None
    startImage: Optional[str] = None
    endImage: Optional[str] = None

    model_config = {"from_attributes": True}
