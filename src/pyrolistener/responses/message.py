from pyrogram.types import Message

from .base import BaseListenResponse


class MessageListenResponse(BaseListenResponse):
    def __init__(self, message: Message) -> None:
        self.message = message
