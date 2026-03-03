from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from ..registry import ListenRegistry
from ..responses import MessageListenResponse


class MessageListenHandler(MessageHandler):
    def __init__(self, listen_registry: ListenRegistry):
        self._listen_registry = listen_registry

        super().__init__(self.callback)

    async def callback(self, client: Client, message: Message) -> None:
        assert message.chat is not None and message.chat.id is not None
        assert message.from_user is not None

        for request in self._listen_registry.get_message_requests():
            if (
                request.message_id is not None
                and (reply_to_message := message.reply_to_message)
                and reply_to_message.id != request.message_id
            ):
                continue

            if (
                request.user_id is not None
                and message.from_user.id != request.user_id
            ):
                continue

            if (
                request.chat_id is not None and message.chat
                and message.chat.id != request.chat_id
            ):
                continue

            if (
                (filters := request.filters)
                and not await filters(client, message)
            ):
                continue

            response = MessageListenResponse(message)
            await request.queue.put(response)

        message.continue_propagation()