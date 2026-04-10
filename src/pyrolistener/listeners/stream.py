import asyncio
from collections.abc import AsyncGenerator, Sequence

from ..registry import ListenRegistry
from ..requests import BaseListenRequest
from ..responses import BaseListenResponse


async def listen_stream(
    listen_registry: ListenRegistry,
    requests: Sequence[BaseListenRequest[BaseListenResponse]]
) -> AsyncGenerator[BaseListenResponse]:
    for request in requests:
        listen_registry.add_request(request)

    response_queue: asyncio.Queue[BaseListenResponse] = asyncio.Queue()

    async def worker(request: BaseListenRequest[BaseListenResponse]) -> None:
        while True:
            response = await request
            await response_queue.put(response)

    try:
        async with asyncio.TaskGroup() as tg:
            for request in requests:
                tg.create_task(worker(request))

            while True:
                yield await response_queue.get()
    finally:
        for request in requests:
            listen_registry.remove_request(request)
