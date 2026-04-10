import asyncio

from pyrogram.filters import Filter

from ..exceptions import ListenTimeoutError
from ..registry import ListenRegistry
from ..responses import (
    CallbackQueryListenResponse,
    MessageListenResponse,
    RawUpdateListenResponse,
)


async def listen_callback_query(
    listen_registry: ListenRegistry,
    *,
    user_id: int | None = None,
    message_id: int | None = None,
    chat_id: int | None = None,
    filters: Filter | None = None,
    timeout: int | float | None = None
) -> CallbackQueryListenResponse:
    request = listen_registry.callback_query_request(
        user_id=user_id,
        message_id=message_id,
        chat_id=chat_id,
        filters=filters
    )

    try:
        response = await asyncio.wait_for(request, timeout)
    except TimeoutError:
        raise ListenTimeoutError from None
    finally:
        listen_registry.remove_callback_query_request(request)

    return response


async def listen_message(
    listen_registry: ListenRegistry,
    *,
    message_id: int | None = None,
    user_id: int | None = None,
    chat_id: int | None = None,
    filters: Filter | None = None,
    timeout: int | float | None = None
) -> MessageListenResponse:
    request = listen_registry.message_request(
        message_id=message_id,
        user_id=user_id,
        chat_id=chat_id,
        filters=filters
    )

    try:
        response = await asyncio.wait_for(request, timeout)
    except TimeoutError:
        raise ListenTimeoutError from None
    finally:
        listen_registry.remove_message_request(request)

    return response

async def listen_raw_update(
    listen_registry: ListenRegistry,
    *,
    timeout: int | float | None = None
) -> RawUpdateListenResponse:
    request = listen_registry.raw_update_request()

    try:
        response = await asyncio.wait_for(request, timeout)
    except TimeoutError:
        raise ListenTimeoutError from None
    finally:
        listen_registry.remove_raw_update_request(request)

    return response
