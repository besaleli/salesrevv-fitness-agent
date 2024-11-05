"""Services."""
from typing import List
from .message import Message

async def pipeline(messages: List[Message]) -> Message:
    """Pipeline."""
    return messages[0]
