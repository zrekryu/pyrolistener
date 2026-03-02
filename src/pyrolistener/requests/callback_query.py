from dataclasses import dataclass

from pyrogram.filters import Filter

from ..responses import CallbackQueryListenResponse
from .base import BaseListenRequest


@dataclass(frozen=True, slots=True)
class CallbackQueryListenRequest(
    BaseListenRequest[CallbackQueryListenResponse]
):
    user_id: int | None = None
    message_id: int | None = None
    chat_id: int | None = None
    filters: Filter | None = None