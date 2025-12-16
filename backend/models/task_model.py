"""Task Model - Data structure for tasks."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Task data model."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    completed: bool = False
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

