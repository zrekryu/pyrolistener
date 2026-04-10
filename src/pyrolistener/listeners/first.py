import asyncio
from collections.abc import Sequence

from ..exceptions import ListenTimeoutError
from ..registry import ListenRegistry
from ..requests import BaseListenRequest
from ..responses import BaseListenResponse


async def listen_first(
    listen_registry: ListenRegistry,
    requests: Sequence[BaseListenRequest[BaseListenResponse]],
    *,
    timeout: int | float | None = None
) -> BaseListenResponse:
    for request in requests:
        listen_registry.add_request(request)

    tasks = {asyncio.ensure_future(request) for request in requests}

    try:
        done, _ = await asyncio.wait(
            tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
        )
    finally:
        for request in requests:
            listen_registry.remove_request(request)

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    if not done:
        raise ListenTimeoutError

    return done.pop().result()
