from pydantic import BaseModel
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum
    priority: PriorityEnum


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    user_id: int

    class Config:
        from_attributes = True