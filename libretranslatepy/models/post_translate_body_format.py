from enum import Enum


class PostTranslateBodyFormat(str, Enum):
    HTML = "html"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
