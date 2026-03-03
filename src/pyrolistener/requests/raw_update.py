from dataclasses import dataclass

from ..responses import RawUpdateListenResponse
from .base import BaseListenRequest


@dataclass(frozen=True, slots=True)
class RawUpdateListenRequest(
    BaseListenRequest[RawUpdateListenResponse]
):
    pass