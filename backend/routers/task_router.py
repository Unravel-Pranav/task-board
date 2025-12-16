"""Task Router - API endpoints for task operations."""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.task_schema import (
    TaskCreateSchema,
    TaskListResponseSchema,
    TaskResponseSchema,
    TaskStatsSchema,
    TaskUpdateSchema,
)
from backend.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponseSchema)
async def get_all_tasks() -> TaskListResponseSchema:
    """Get all tasks with statistics."""
    data = task_service.get_tasks_with_stats()
    return TaskListResponseSchema(**data)


@router.post("", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema) -> TaskResponseSchema:
    """Create a new task."""
    task = task_service.create_task(
        title=task_data.title,
        priority=task_data.priority.value
    )
    return TaskResponseSchema(**task.to_dict())


@router.get("/stats", response_model=TaskStatsSchema)
async def get_task_stats() -> TaskStatsSchema:
    """Get task statistics."""
    stats = task_service.get_task_stats()
    return TaskStatsSchema(**stats)


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(task_id: str) -> TaskResponseSchema:
    """Get a single task by ID."""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    return TaskResponseSchema(**task.to_dict())


@router.patch("/{task_id}", response_model=TaskResponseSchema)
async def update_task(task_id: str, task_data: TaskUpdateSchema) -> TaskResponseSchema:
    """Update a task."""
    task = task_service.update_task(
        task_id=task_id,
        title=task_data.title,
        completed=task_data.completed,
        priority=task_data.priority.value if task_data.priority else None
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    return TaskResponseSchema(**task.to_dict())


@router.patch("/{task_id}/toggle", response_model=TaskResponseSchema)
async def toggle_task_completion(task_id: str) -> TaskResponseSchema:
    """Toggle task completion status."""
    task = task_service.toggle_task_completion(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    return TaskResponseSchema(**task.to_dict())


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str) -> None:
    """Delete a task."""
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_tasks() -> None:
    """Clear all tasks."""
    task_service.clear_all_tasks()

