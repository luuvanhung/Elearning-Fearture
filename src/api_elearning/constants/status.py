from enum import Enum


class AssignmentStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    OPEN = "OPEN"

    @classmethod
    def choices(cls):
        return ((status.name, status.value) for status in cls)


class AssignmentContentStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    OPEN = "OPEN"
    LOCK = "LOCK"

    @classmethod
    def choices(cls):
        return ((status.name, status.value) for status in cls)
