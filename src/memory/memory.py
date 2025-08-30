from collections import deque
from typing import Deque, Dict, List

class ConversationBuffer:
    def __init__(self, max_turns: int = 10):
        self.buffer: Deque[Dict[str, str]] = deque(maxlen=max_turns)

    def add_user(self, content: str):
        self.buffer.append({"role": "user", "content": content})

    def add_ai(self, content: str):
        self.buffer.append({"role": "assistant", "content": content})

    def history(self) -> List[Dict[str, str]]:
        return list(self.buffer)
