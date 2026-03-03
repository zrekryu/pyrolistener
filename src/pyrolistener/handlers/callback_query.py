from pyrogram import Client
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import CallbackQuery

from ..registry import ListenRegistry
from ..responses import CallbackQueryListenResponse


class CallbackQueryListenHandler(CallbackQueryHandler):
    def __init__(self, listen_registry: ListenRegistry):
        self._listen_registry = listen_registry

        super().__init__(self.callback)

    async def callback(self, client: Client, callback_query: CallbackQuery) -> None:
        for request in self._listen_registry.get_callback_query_requests():
            message = callback_query.message

            if (
                request.user_id is not None
                and callback_query.from_user.id != request.user_id
            ):
                continue

            if (
                request.message_id is not None and message
                and message.id != request.message_id
            ):
                continue

            if (
                request.chat_id is not None and message
                and (chat := message.chat)
                and chat.id != request.chat_id
            ):
                continue

            if (
                (filters := request.filters)
                and not await filters(client, callback_query)
            ):
                continue

            response = CallbackQueryListenResponse(callback_query)
            await request.queue.put(response)

        callback_query.continue_propagation()