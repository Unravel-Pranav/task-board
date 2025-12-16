"""Tests for Task Service."""

import pytest

from backend.models.task_model import TaskPriority
from backend.services.task_service import TaskService


@pytest.fixture
def task_service():
    """Create a fresh task service for each test."""
    service = TaskService()
    service.clear_all_tasks()  # Start with clean state
    return service


class TestTaskService:
    """Test cases for TaskService."""

    def test_create_task(self, task_service: TaskService) -> None:
        """Test creating a new task."""
        task = task_service.create_task("Test Task", "high")

        assert task.title == "Test Task"
        assert task.priority == TaskPriority.HIGH
        assert task.completed is False
        assert task.id is not None

    def test_create_task_with_whitespace(self, task_service: TaskService) -> None:
        """Test creating task trims whitespace."""
        task = task_service.create_task("  Trimmed Task  ", "medium")

        assert task.title == "Trimmed Task"

    def test_get_all_tasks(self, task_service: TaskService) -> None:
        """Test getting all tasks."""
        task_service.create_task("Task 1")
        task_service.create_task("Task 2")

        tasks = task_service.get_all_tasks()

        assert len(tasks) == 2

    def test_get_task(self, task_service: TaskService) -> None:
        """Test getting a specific task."""
        created = task_service.create_task("Find Me")

        found = task_service.get_task(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.title == "Find Me"

    def test_get_task_not_found(self, task_service: TaskService) -> None:
        """Test getting non-existent task."""
        found = task_service.get_task("non-existent-id")

        assert found is None

    def test_toggle_task_completion(self, task_service: TaskService) -> None:
        """Test toggling task completion."""
        task = task_service.create_task("Toggle Me")
        assert task.completed is False

        toggled = task_service.toggle_task_completion(task.id)

        assert toggled is not None
        assert toggled.completed is True
        assert toggled.completed_at is not None

    def test_toggle_task_twice(self, task_service: TaskService) -> None:
        """Test toggling task completion twice."""
        task = task_service.create_task("Toggle Twice")

        task_service.toggle_task_completion(task.id)
        toggled = task_service.toggle_task_completion(task.id)

        assert toggled is not None
        assert toggled.completed is False
        assert toggled.completed_at is None

    def test_delete_task(self, task_service: TaskService) -> None:
        """Test deleting a task."""
        task = task_service.create_task("Delete Me")

        result = task_service.delete_task(task.id)

        assert result is True
        assert task_service.get_task(task.id) is None

    def test_delete_task_not_found(self, task_service: TaskService) -> None:
        """Test deleting non-existent task."""
        result = task_service.delete_task("non-existent-id")

        assert result is False

    def test_get_task_stats(self, task_service: TaskService) -> None:
        """Test getting task statistics."""
        task_service.create_task("Task 1", "high")
        task_service.create_task("Task 2", "medium")
        task3 = task_service.create_task("Task 3", "low")
        task_service.toggle_task_completion(task3.id)

        stats = task_service.get_task_stats()

        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["pending"] == 2
        assert stats["progress_percentage"] == pytest.approx(33.33, rel=0.1)
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["medium"] == 1
        assert stats["by_priority"]["low"] == 1

    def test_get_tasks_with_stats(self, task_service: TaskService) -> None:
        """Test getting tasks with statistics."""
        task_service.create_task("Task 1")
        task_service.create_task("Task 2")

        result = task_service.get_tasks_with_stats()

        assert "tasks" in result
        assert len(result["tasks"]) == 2
        assert result["total"] == 2
        assert result["completed"] == 0
        assert result["pending"] == 2
        assert result["progress_percentage"] == 0

    def test_update_task(self, task_service: TaskService) -> None:
        """Test updating a task."""
        task = task_service.create_task("Original", "low")

        updated = task_service.update_task(
            task.id,
            title="Updated",
            priority="high"
        )

        assert updated is not None
        assert updated.title == "Updated"
        assert updated.priority == TaskPriority.HIGH

