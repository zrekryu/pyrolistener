from pyrogram import raw

from .base import BaseListenResponse


class RawUpdateListenResponse(BaseListenResponse):
    def __init__(
        self,
        update: raw.base.Update,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.Chat]
    ) -> None:
        self.update = update
        self.users = users
        self.chats = chats