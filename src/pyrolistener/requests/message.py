from dataclasses import dataclass

from pyrogram.filters import Filter

from ..responses import MessageListenResponse
from .base import BaseListenRequest


@dataclass(frozen=True, slots=True)
class MessageListenRequest(
    BaseListenRequest[MessageListenResponse]
):
    message_id: int | None = None
    user_id: int | None = None
    chat_id: int | None = None
    filters: Filter | None = None