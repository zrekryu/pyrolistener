from pyrogram import Client, ContinuePropagation, raw
from pyrogram.handlers import RawUpdateHandler

from ..registry import ListenRegistry
from ..responses import RawUpdateListenResponse


class RawUpdateListenHandler(RawUpdateHandler):
    def __init__(self, listen_registry: ListenRegistry):
        self._listen_registry = listen_registry

        super().__init__(self.callback)

    async def callback(
        self,
        client: Client,
        update: raw.base.Update,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.Chat]
    ) -> None:
        for request in self._listen_registry.get_raw_update_requests():
            response = RawUpdateListenResponse(update, users, chats)
            await request.queue.put(response)

        raise ContinuePropagation