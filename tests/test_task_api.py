"""Tests for Task API endpoints."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.task_service import task_service


@pytest.fixture
def client():
    """Create a test client."""
    task_service.clear_all_tasks()  # Start with clean state
    return TestClient(app)


class TestTaskAPI:
    """Test cases for Task API endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_get_empty_tasks(self, client: TestClient) -> None:
        """Test getting tasks when none exist."""
        response = client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0
        assert data["progress_percentage"] == 0

    def test_create_task(self, client: TestClient) -> None:
        """Test creating a new task."""
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "priority": "high"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["priority"] == "high"
        assert data["completed"] is False

    def test_create_task_default_priority(self, client: TestClient) -> None:
        """Test creating task with default priority."""
        response = client.post(
            "/api/tasks",
            json={"title": "Default Priority Task"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["priority"] == "medium"

    def test_get_tasks(self, client: TestClient) -> None:
        """Test getting all tasks."""
        client.post("/api/tasks", json={"title": "Task 1"})
        client.post("/api/tasks", json={"title": "Task 2"})

        response = client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["tasks"]) == 2

    def test_get_single_task(self, client: TestClient) -> None:
        """Test getting a single task."""
        create_response = client.post("/api/tasks", json={"title": "Find Me"})
        task_id = create_response.json()["id"]

        response = client.get(f"/api/tasks/{task_id}")

        assert response.status_code == 200
        assert response.json()["title"] == "Find Me"

    def test_get_task_not_found(self, client: TestClient) -> None:
        """Test getting non-existent task."""
        response = client.get("/api/tasks/non-existent-id")

        assert response.status_code == 404

    def test_toggle_task(self, client: TestClient) -> None:
        """Test toggling task completion."""
        create_response = client.post("/api/tasks", json={"title": "Toggle Me"})
        task_id = create_response.json()["id"]

        response = client.patch(f"/api/tasks/{task_id}/toggle")

        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_task(self, client: TestClient) -> None:
        """Test updating a task."""
        create_response = client.post("/api/tasks", json={"title": "Original"})
        task_id = create_response.json()["id"]

        response = client.patch(
            f"/api/tasks/{task_id}",
            json={"title": "Updated", "priority": "high"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["priority"] == "high"

    def test_delete_task(self, client: TestClient) -> None:
        """Test deleting a task."""
        create_response = client.post("/api/tasks", json={"title": "Delete Me"})
        task_id = create_response.json()["id"]

        response = client.delete(f"/api/tasks/{task_id}")

        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent task."""
        response = client.delete("/api/tasks/non-existent-id")

        assert response.status_code == 404

    def test_get_stats(self, client: TestClient) -> None:
        """Test getting task statistics."""
        client.post("/api/tasks", json={"title": "Task 1", "priority": "high"})
        client.post("/api/tasks", json={"title": "Task 2", "priority": "low"})

        # Complete one task
        tasks_response = client.get("/api/tasks")
        task_id = tasks_response.json()["tasks"][0]["id"]
        client.patch(f"/api/tasks/{task_id}/toggle")

        response = client.get("/api/tasks/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["completed"] == 1
        assert data["pending"] == 1

    def test_create_task_validation_error(self, client: TestClient) -> None:
        """Test creating task with invalid data."""
        response = client.post("/api/tasks", json={"title": ""})

        assert response.status_code == 422

