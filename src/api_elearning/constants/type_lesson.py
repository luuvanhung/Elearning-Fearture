from enum import Enum


class TypeLesson(Enum):
    VIDEO = "VIDEO"
    DOCS = "DOCS"
    SLIDE = "SLIDE"

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
