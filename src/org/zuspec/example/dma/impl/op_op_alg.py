
import zuspec.dataclasses as zdc
from typing import Dict, List

from ..mem import MemoryOp
from ..op import DmaOp, MemCpy, DevCpy
from ..req import ReqOp


@zdc.dataclass
class DmaOpOpAlg(DmaOp, ReqOp, zdc.Component):
    """DMA engine with no fixed channels. Uses MemoryOp for memory access
    and implements ReqOp for device transfer request control."""
    
    mem: MemoryOp = zdc.port()
    
    _mem_l: zdc.Lock = zdc.field()
    # Map of req_id -> Event for device transfer synchronization
    _req_events: Dict[zdc.i32, zdc.Event] = zdc.field(default_factory=dict)

    async def req_transfer(self, id: zdc.i32):
        """Request a transfer for the given id."""
        if id in self._req_events:
            self._req_events[id].set()

    async def memcpy(
            self,
            src: zdc.uptr,
            dst: zdc.uptr,
            sz: zdc.u32,
            pri: zdc.i32 = 0):
        """Copy memory from src to dst.
        
        Performs narrow accesses until 8-byte aligned, then wide accesses.
        """
        await self._mem_l.acquire()
        try:
            remaining = sz
            while remaining > 0:
                # Determine access size based on alignment and remaining bytes
                # Use the largest power-of-2 size that is both aligned and fits
                align = src & 0x7  # Low 3 bits give alignment
                if align == 0 and remaining >= 8:
                    xfer_sz = 8
                elif (align & 0x3) == 0 and remaining >= 4:
                    xfer_sz = 4
                elif (align & 0x1) == 0 and remaining >= 2:
                    xfer_sz = 2
                else:
                    xfer_sz = 1
                
                data = await self.mem.read(src)
                await self.mem.write(dst, data, xfer_sz)
                src += xfer_sz
                dst += xfer_sz
                remaining -= xfer_sz
        finally:
            self._mem_l.release()

    async def memcpy_chain(
            self,
            xfers: List[MemCpy],
            pri: zdc.i32 = 0):
        """Execute a chain of memory copies."""
        for xfer in xfers:
            await self.memcpy(xfer.src, xfer.dst, xfer.sz, pri)

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
        """Device copy with chunk-based request synchronization."""
        # Create event for this request id
        ev = zdc.Event()
        self._req_events[req_id] = ev
        
        try:
            remaining = sz
            while remaining > 0:
                # Wait for device to request a chunk
                await ev.wait()
                ev.clear()
                
                # Transfer one chunk
                chunk_bytes = chk_sz * acc_sz
                xfer_bytes = min(chunk_bytes, remaining)
                
                await self._mem_l.acquire()
                try:
                    chunk_remaining = xfer_bytes
                    while chunk_remaining > 0:
                        data = await self.mem.read(src)
                        await self.mem.write(dst, data, acc_sz)
                        if inc_src:
                            src += acc_sz
                        if inc_dst:
                            dst += acc_sz
                        chunk_remaining -= acc_sz
                finally:
                    self._mem_l.release()
                
                remaining -= xfer_bytes
        finally:
            del self._req_events[req_id]

    async def devcpy_chain(
            self,
            xfers: List[DevCpy],
            req_id: zdc.i32,
            pri: zdc.i32 = 0):
        """Execute a chain of device copies sharing the same req_id."""
        # Create event for this request id
        ev = zdc.Event()
        self._req_events[req_id] = ev
        
        try:
            for xfer in xfers:
                src = xfer.src
                dst = xfer.dst
                remaining = xfer.sz
                
                while remaining > 0:
                    # Wait for device to request a chunk
                    await ev.wait()
                    ev.clear()
                    
                    # Transfer one chunk
                    chunk_bytes = xfer.chk_sz * xfer.acc_sz
                    xfer_bytes = min(chunk_bytes, remaining)
                    
                    await self._mem_l.acquire()
                    try:
                        chunk_remaining = xfer_bytes
                        while chunk_remaining > 0:
                            data = await self.mem.read(src)
                            await self.mem.write(dst, data, xfer.acc_sz)
                            if xfer.inc_src:
                                src += xfer.acc_sz
                            if xfer.inc_dst:
                                dst += xfer.acc_sz
                            chunk_remaining -= xfer.acc_sz
                    finally:
                        self._mem_l.release()
                    
                    remaining -= xfer_bytes
        finally:
            del self._req_events[req_id]

