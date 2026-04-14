# from pydantic import BaseModel, Field
# from typing import List

# class ExerciseSchema(BaseModel):
#     name: str = Field(..., example="3/4 Sit-Up")
#     force: str = Field(..., example="pull")  # force direction used during movement
#     level: str = Field(..., example="beginner")  # difficulty level
#     mechanic: str = Field(..., example="compound")  # movement type
#     equipment: str = Field(..., example="body only")  # required equipment
#     primaryMuscles: List[str] = Field(default_factory=list)
#     secondaryMuscles: List[str] = Field(default_factory=list)
#     instructions: List[str] = Field(default_factory=list)
#     category: str = Field(..., example="strength")  # training category

#     class Config:
#         orm_mode = True


# from pydantic import BaseModel
# from typing import List, Optional

# class ExerciseSchema(BaseModel):
#     id: int
#     name: str
#     force: Optional[str]
#     level: Optional[str]
#     mechanic: Optional[str]
#     equipment: Optional[str]
#     primaryMuscles: Optional[List[str]]
#     secondaryMuscles: Optional[List[str]]
#     instructions: Optional[List[str]]
#     category: Optional[str]

#     class Config:
#         orm_mode = True
from pydantic import BaseModel
from typing import Optional, List

class ExerciseSchema(BaseModel):
    id: int
    name: str
    force: Optional[str]
    level: Optional[str]
    mechanic: Optional[str]
    equipment: Optional[str]
    primaryMuscles: Optional[List[str]]
    secondaryMuscles: Optional[List[str]]
    instructions: Optional[List[str]]
    category: Optional[str]
    startImage: Optional[str]
    endImage: Optional[str]

    class Config:
        orm_mode = True