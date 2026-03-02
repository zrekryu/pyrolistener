from pyrogram.types import CallbackQuery

from .base import BaseListenResponse


class CallbackQueryListenResponse(BaseListenResponse):
    def __init__(self, callback_query: CallbackQuery) -> None:
        self.callback_query = callback_query
