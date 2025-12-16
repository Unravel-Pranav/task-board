"""Task Schemas - Pydantic models for request/response validation."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TaskPriorityEnum(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    priority: TaskPriorityEnum = Field(default=TaskPriorityEnum.MEDIUM, description="Task priority")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: str | None = Field(None, min_length=1, max_length=200)
    completed: bool | None = None
    priority: TaskPriorityEnum | None = None


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    title: str
    completed: bool
    priority: TaskPriorityEnum
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class TaskListResponseSchema(BaseModel):
    """Schema for task list response with statistics."""
    tasks: list[TaskResponseSchema]
    total: int
    completed: int
    pending: int
    progress_percentage: float


class TaskStatsSchema(BaseModel):
    """Schema for task statistics."""
    total: int
    completed: int
    pending: int
    progress_percentage: float
    by_priority: dict[str, int]
    completed_today: int

