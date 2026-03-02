import asyncio
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import Any

from ..responses import BaseListenResponse


@dataclass(frozen=True, slots=True)
class BaseListenRequest[R: BaseListenResponse]:
    queue: asyncio.Queue[R] = field(
        init=False, default_factory=asyncio.Queue[R]
    )

    def __await__(self) -> Generator[Any, Any, R]:
        return self.queue.get().__await__()