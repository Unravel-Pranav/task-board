"""Task Service - Business logic layer for tasks."""

from typing import Any

from backend.models.task_model import Task, TaskPriority
from backend.repositories.task_repo import task_repository


class TaskService:
    """Service layer for task business logic."""

    def __init__(self) -> None:
        """Initialize service with repository."""
        self._repo = task_repository

    def create_task(self, title: str, priority: str = "medium") -> Task:
        """Create a new task with validation."""
        # Validate and convert priority
        try:
            task_priority = TaskPriority(priority)
        except ValueError:
            task_priority = TaskPriority.MEDIUM

        return self._repo.create(title=title.strip(), priority=task_priority)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks."""
        return self._repo.get_all()

    def get_task(self, task_id: str) -> Task | None:
        """Get a single task by ID."""
        return self._repo.get_by_id(task_id)

    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        completed: bool | None = None,
        priority: str | None = None
    ) -> Task | None:
        """Update a task."""
        task_priority = None
        if priority:
            try:
                task_priority = TaskPriority(priority)
            except ValueError:
                pass

        return self._repo.update(
            task_id=task_id,
            title=title.strip() if title else None,
            completed=completed,
            priority=task_priority
        )

    def toggle_task_completion(self, task_id: str) -> Task | None:
        """Toggle task completion status."""
        task = self._repo.get_by_id(task_id)
        if not task:
            return None

        return self._repo.update(task_id=task_id, completed=not task.completed)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        return self._repo.delete(task_id)

    def get_task_stats(self) -> dict[str, Any]:
        """Get task statistics."""
        return self._repo.get_stats()

    def get_tasks_with_stats(self) -> dict[str, Any]:
        """Get all tasks with statistics."""
        tasks = self._repo.get_all()
        stats = self._repo.get_stats()

        return {
            "tasks": [task.to_dict() for task in tasks],
            "total": stats["total"],
            "completed": stats["completed"],
            "pending": stats["pending"],
            "progress_percentage": stats["progress_percentage"],
        }

    def clear_all_tasks(self) -> None:
        """Clear all tasks."""
        self._repo.clear_all()


# Singleton service instance
task_service = TaskService()

