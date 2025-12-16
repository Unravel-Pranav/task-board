"""Task Repository - Data access layer for tasks."""

from datetime import datetime
from typing import Any

from backend.models.task_model import Task, TaskPriority


class TaskRepository:
    """Repository for task data operations - In-memory storage."""

    def __init__(self) -> None:
        """Initialize the repository with empty storage."""
        self._tasks: dict[str, Task] = {}

    def create(self, title: str, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Create a new task."""
        task = Task(title=title, priority=priority)
        self._tasks[task.id] = task
        return task

    def get_all(self) -> list[Task]:
        """Get all tasks sorted by creation date."""
        return sorted(
            self._tasks.values(),
            key=lambda t: t.created_at,
            reverse=True
        )

    def get_by_id(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def update(
        self,
        task_id: str,
        title: str | None = None,
        completed: bool | None = None,
        priority: TaskPriority | None = None
    ) -> Task | None:
        """Update a task."""
        task = self._tasks.get(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title

        if completed is not None:
            task.completed = completed
            task.completed_at = datetime.now() if completed else None

        if priority is not None:
            task.priority = priority

        return task

    def delete(self, task_id: str) -> bool:
        """Delete a task by ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_stats(self) -> dict[str, Any]:
        """Get task statistics."""
        tasks = list(self._tasks.values())
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        pending = total - completed

        # Count by priority
        by_priority = {
            "low": sum(1 for t in tasks if t.priority == TaskPriority.LOW),
            "medium": sum(1 for t in tasks if t.priority == TaskPriority.MEDIUM),
            "high": sum(1 for t in tasks if t.priority == TaskPriority.HIGH),
        }

        # Completed today
        today = datetime.now().date()
        completed_today = sum(
            1 for t in tasks
            if t.completed and t.completed_at and t.completed_at.date() == today
        )

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "progress_percentage": (completed / total * 100) if total > 0 else 0,
            "by_priority": by_priority,
            "completed_today": completed_today,
        }

    def clear_all(self) -> None:
        """Clear all tasks."""
        self._tasks.clear()


# Singleton instance for in-memory storage
task_repository = TaskRepository()

