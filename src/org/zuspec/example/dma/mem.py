import zuspec.dataclasses as zdc
from typing import Protocol


class MemoryOp(Protocol):
    """Memory interface for DMA to access system memory."""

    async def read(self, addr: zdc.u64) -> zdc.u64:
        """Read a word from memory.

        Args:
            addr: Memory address (word-aligned)

        Returns:
            Data value read
        """
        ...

    async def write(self, addr: zdc.u64, data: zdc.u64, size: zdc.i8) -> None:
        """Write a word to memory.

        Args:
            addr: Memory address (word-aligned)
            data: Data value to write
        """
        ...
