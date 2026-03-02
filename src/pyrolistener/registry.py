from collections.abc import Generator

from pyrogram.filters import Filter

from .requests import CallbackQueryListenRequest, MessageListenRequest


class ListenRegistry:
    def __init__(self) -> None:
        self._message_requests: list[MessageListenRequest] = []
        self._callback_query_requests: list[CallbackQueryListenRequest] = []

    def add_message_request(self, request: MessageListenRequest) -> None:
        self._message_requests.append(request)

    def remove_message_request(self, request: MessageListenRequest) -> None:
        try:
            self._message_requests.remove(request)
        except IndexError:
            raise ValueError("Message listen request not found") from None

    def get_message_requests(self) -> Generator[MessageListenRequest]:
        yield from self._message_requests

    def message_request(
        self,
        message_id: int | None = None,
        user_id: int | None = None,
        chat_id: int | None = None,
        filters: Filter | None = None
    ) -> MessageListenRequest:
        request = MessageListenRequest(
            message_id=message_id,
            user_id=user_id,
            chat_id=chat_id,
            filters=filters
        )
        self.add_message_request(request)

        return request

    def add_callback_query_request(self, request: CallbackQueryListenRequest) -> None:
        self._callback_query_requests.append(request)

    def remove_callback_query_request(
        self, request: CallbackQueryListenRequest
    ) -> None:
        try:
            self._callback_query_requests.remove(request)
        except IndexError:
            raise ValueError("Callback query listen request not found") from None

    def get_callback_query_requests(self) -> Generator[CallbackQueryListenRequest]:
        yield from self._callback_query_requests

    def callback_query_request(
        self,
        user_id: int | None = None,
        message_id: int | None = None,
        chat_id: int | None = None,
        filters: Filter | None = None
    ) -> CallbackQueryListenRequest:
        request = CallbackQueryListenRequest(
            user_id=user_id,
            message_id=message_id,
            chat_id=chat_id,
            filters=filters
        )
        self.add_callback_query_request(request)

        return request
