from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class ChatMessage:
    type: str
    content: str
    name: Optional[str]

    def __init__(self, type: str, content: str, name: Optional[str] = None):
        self.type = type
        self.content = content
        self.name = name

    def __str__(self):
        return (f"""
            ChatMessage(
                type={self.type},
                content={self.content},
                name={self.name}
        """)

    def __dict__(self):
        return {
            "type": self.type,
            "content": self.content,
            "name": self.name
        }