import zuspec.dataclasses as zdc
from typing import List, Protocol

@zdc.dataclass
class MemCpy(zdc.Struct):
    src: zdc.uptr = zdc.field()
    dst: zdc.uptr = zdc.field()
    sz: zdc.u32 = zdc.field()

@zdc.dataclass
class DevCpy(MemCpy):
    acc_sz: zdc.u8 = zdc.field()
    chk_sz: zdc.u32 = zdc.field()
    inc_src: bool = zdc.field()
    inc_dst: bool = zdc.field()


class DmaOp(Protocol):

    async def memcpy(
            self,
            src: zdc.uptr,
            dst: zdc.uptr,
            sz: zdc.u32,
            pri: zdc.i32 = 0):
        ...

    async def memcpy_chain(
            self,
            xfers: List[MemCpy],
            pri: zdc.i32 = 0):
        ...

    async def devcpy(
            self,
            src: zdc.uptr,
            dst: zdc.uptr,
            sz: zdc.u32,
            acc_sz: zdc.u8,
            chk_sz: zdc.u32,
            inc_src: bool,
            inc_dst: bool,
            req_id: zdc.i32,
            pri: zdc.i32 = 0):
        ...

    async def devcpy_chain(
            self,
            xfers: List[DevCpy],
            req_id: zdc.i32,
            pri: zdc.i32 = 0):
        ...

