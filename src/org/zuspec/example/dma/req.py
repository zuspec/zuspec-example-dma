
import zuspec.dataclasses as zdc
from typing import Protocol


class ReqOp(Protocol):
    async def req_transfer(self, id: zdc.i32):
        """Request a transfer"""
        ...