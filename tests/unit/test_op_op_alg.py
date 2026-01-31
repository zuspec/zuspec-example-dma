#!/usr/bin/env python3
# ****************************************************************************
#  Unit Tests for DmaOpOpAlg (op_op_alg.py)
# ****************************************************************************

import sys
import os
import asyncio
from dataclasses import dataclass as py_dataclass

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__),
    '../../packages/zuspec-dataclasses/src'))

import zuspec.dataclasses as zdc  # noqa: E402
from org.zuspec.example.dma.op import DmaOp  # noqa: E402
from org.zuspec.example.dma.impl.op_op_alg import DmaOpOpAlg  # noqa: E402
from org.zuspec.example.dma.mem import MemoryOp  # noqa: E402
from org.zuspec.example.dma.req import ReqOp  # noqa: E402


# =============================================================================
# Test Data Classes (plain Python dataclasses for test use)
# =============================================================================

@py_dataclass
class MemCpyTest:
    """Test data class for memory copy operations."""
    src: int
    dst: int
    sz: int


@py_dataclass
class DevCpyTest:
    """Test data class for device copy operations."""
    src: int
    dst: int
    sz: int
    acc_sz: int
    chk_sz: int
    inc_src: bool
    inc_dst: bool


# =============================================================================
# Mock Memory Implementation
# =============================================================================

@zdc.dataclass
class MockMemory(zdc.Component):
    """Mock memory for testing DMA operations.
    
    Uses byte-addressable storage to properly handle different access sizes.
    Includes configurable access delay.
    """
    
    read_delay: zdc.Time = zdc.field(default=None)
    write_delay: zdc.Time = zdc.field(default=None)

    def __post_init__(self):
        self.storage = {}  # byte-addressable: addr -> byte value

    async def read(self, addr: zdc.u64) -> zdc.u64:
        """Read up to 8 bytes from memory, returning as u64."""
        if self.read_delay is not None:
            await self.wait(self.read_delay)
        result = 0
        for i in range(8):
            byte_val = self.storage.get(addr + i, 0)
            result |= (byte_val & 0xFF) << (i * 8)
        return result

    async def write(self, addr: zdc.u64, data: zdc.u64, size: zdc.i8) -> None:
        """Write 'size' bytes to memory starting at addr."""
        if self.write_delay is not None:
            await self.wait(self.write_delay)
        for i in range(size):
            self.storage[addr + i] = (data >> (i * 8)) & 0xFF


# =============================================================================
# Test Fixture: DMA with Memory
# =============================================================================

@zdc.dataclass
class DmaTestFixture(zdc.Component):
    """Test fixture that groups DMA engine with mock memory."""
    
    mem: MockMemory = zdc.field()
    dma: DmaOpOpAlg = zdc.field()

    def __bind__(self):
        return {
            self.dma.mem: self.mem
        }

    def init_memory(self, base_addr: int, data: list, word_size: int = 8):
        """Initialize memory with data starting at base_addr.
        
        Args:
            base_addr: Starting address
            data: List of word values
            word_size: Size of each word in bytes (default 8)
        """
        for i, val in enumerate(data):
            addr = base_addr + i * word_size
            for b in range(word_size):
                self.mem.storage[addr + b] = (val >> (b * 8)) & 0xFF

    def read_memory(self, base_addr: int, count: int, word_size: int = 8) -> list:
        """Read count words from memory starting at base_addr.
        
        Args:
            base_addr: Starting address
            count: Number of words to read
            word_size: Size of each word in bytes (default 8)
        """
        result = []
        for i in range(count):
            addr = base_addr + i * word_size
            val = 0
            for b in range(word_size):
                val |= self.mem.storage.get(addr + b, 0) << (b * 8)
            result.append(val)
        return result

    def clear_memory(self):
        """Clear all memory."""
        self.mem.storage.clear()


# =============================================================================
# Basic Structure Tests
# =============================================================================

def test_dma_implements_interfaces():
    """Test that DmaOpOpAlg implements DmaOp and ReqOp interfaces."""
    print("\n=== Test: DMA Implements Interfaces ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            dma = self.fixture.dma
            
            # Check DmaOp methods
            assert hasattr(dma, 'memcpy'), "Should have memcpy"
            assert hasattr(dma, 'memcpy_chain'), "Should have memcpy_chain"
            assert hasattr(dma, 'devcpy'), "Should have devcpy"
            assert hasattr(dma, 'devcpy_chain'), "Should have devcpy_chain"
            
            # Check ReqOp methods
            assert hasattr(dma, 'req_transfer'), "Should have req_transfer"
            
            print("  DMA implements interfaces test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_dma_has_memory_port():
    """Test that DMA has a memory port."""
    print("\n=== Test: DMA Has Memory Port ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            dma = self.fixture.dma
            assert hasattr(dma, 'mem'), "Should have mem port"
            print("  DMA has memory port test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# memcpy Tests
# =============================================================================

def test_memcpy_basic():
    """Test basic memcpy operation."""
    print("\n=== Test: Basic memcpy ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize source memory
            data = [0x10, 0x20, 0x30, 0x40]
            self.fixture.init_memory(0x1000, data)

            # Perform memcpy
            await self.fixture.dma.memcpy(
                src=0x1000,
                dst=0x2000,
                sz=32  # 4 words * 8 bytes
            )

            # Verify destination
            result = self.fixture.read_memory(0x2000, 4)
            assert result == data, f"Data mismatch: {result} != {data}"

            print("  Basic memcpy test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_memcpy_with_priority():
    """Test memcpy with priority parameter."""
    print("\n=== Test: memcpy with priority ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            data = [0xAA, 0xBB]
            self.fixture.init_memory(0x1000, data)

            # Perform memcpy with priority
            await self.fixture.dma.memcpy(
                src=0x1000,
                dst=0x2000,
                sz=16,
                pri=5
            )

            result = self.fixture.read_memory(0x2000, 2)
            assert result == data, f"Data mismatch: {result} != {data}"

            print("  memcpy with priority test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_memcpy_large_transfer():
    """Test memcpy with larger transfer."""
    print("\n=== Test: Large memcpy ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize 64 words
            data = list(range(64))
            self.fixture.init_memory(0x1000, data)

            # Perform memcpy
            await self.fixture.dma.memcpy(
                src=0x1000,
                dst=0x2000,
                sz=64 * 8
            )

            result = self.fixture.read_memory(0x2000, 64)
            assert result == data, "Large transfer data mismatch"

            print("  Large memcpy test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_memcpy_unaligned():
    """Test memcpy with unaligned addresses uses proper access sizes."""
    print("\n=== Test: Unaligned memcpy ===")

    @zdc.dataclass
    class TrackingMemory(zdc.Component):
        """Memory that tracks access sizes."""

        def __post_init__(self):
            self.storage = {}
            self.write_sizes = []  # Track (addr, size) for each write

        async def read(self, addr: zdc.u64) -> zdc.u64:
            result = 0
            for i in range(8):
                byte_val = self.storage.get(addr + i, 0)
                result |= (byte_val & 0xFF) << (i * 8)
            return result

        async def write(self, addr: zdc.u64, data: zdc.u64, size: zdc.i8) -> None:
            self.write_sizes.append((addr, size))
            for i in range(size):
                self.storage[addr + i] = (data >> (i * 8)) & 0xFF

    @zdc.dataclass
    class Top(zdc.Component):
        mem: TrackingMemory = zdc.field()
        dma: DmaOpOpAlg = zdc.field()

        def __bind__(self):
            return {self.dma.mem: self.mem}

        async def run(self):
            # Initialize source data (11 bytes starting at unaligned address)
            for i in range(11):
                self.mem.storage[0x1001 + i] = 0xAA + i

            # Copy 11 bytes from 0x1001 (unaligned) to 0x2001 (unaligned)
            await self.dma.memcpy(src=0x1001, dst=0x2001, sz=11)

            # Verify data was copied correctly
            for i in range(11):
                expected = 0xAA + i
                actual = self.mem.storage.get(0x2001 + i, 0)
                assert actual == expected, f"Byte {i}: {actual:#x} != {expected:#x}"

            # Check access pattern: should start narrow, go wide, end narrow
            # 0x1001: 1 byte to reach 0x1002
            # 0x1002: 2 bytes to reach 0x1004
            # 0x1004: 4 bytes to reach 0x1008
            # 0x1008: 4 bytes (only 4 remaining, not 8)
            # Total: 1 + 2 + 4 + 4 = 11 bytes
            sizes = [s for (_, s) in self.mem.write_sizes]
            print(f"  Access sizes: {sizes}")
            
            # Verify we used appropriate sizes (not all 1-byte accesses)
            assert 4 in sizes or 8 in sizes, "Should use wide accesses when aligned"
            assert 1 in sizes or 2 in sizes, "Should use narrow accesses for unaligned portions"
            
            # Verify total bytes transferred
            total = sum(sizes)
            assert total == 11, f"Total bytes: {total} != 11"

            print("  Unaligned memcpy test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# memcpy_chain Tests
# =============================================================================

def test_memcpy_chain_basic():
    """Test basic memcpy_chain operation."""
    print("\n=== Test: Basic memcpy_chain ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize two source regions
            data1 = [0x11, 0x22]
            data2 = [0x33, 0x44]
            self.fixture.init_memory(0x1000, data1)
            self.fixture.init_memory(0x3000, data2)

            # Create chain of transfers
            xfers = [
                MemCpyTest(src=0x1000, dst=0x2000, sz=16),
                MemCpyTest(src=0x3000, dst=0x4000, sz=16)
            ]

            await self.fixture.dma.memcpy_chain(xfers)

            # Verify both destinations
            result1 = self.fixture.read_memory(0x2000, 2)
            result2 = self.fixture.read_memory(0x4000, 2)
            assert result1 == data1, f"First transfer mismatch: {result1}"
            assert result2 == data2, f"Second transfer mismatch: {result2}"

            print("  Basic memcpy_chain test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_memcpy_chain_multiple():
    """Test memcpy_chain with multiple transfers."""
    print("\n=== Test: Multiple memcpy_chain ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize 4 source regions
            for i in range(4):
                self.fixture.init_memory(0x1000 + i * 0x1000, [i * 10 + j for j in range(4)])

            # Create chain of 4 transfers
            xfers = [
                MemCpyTest(src=0x1000 + i * 0x1000, dst=0x5000 + i * 0x1000, sz=32)
                for i in range(4)
            ]

            await self.fixture.dma.memcpy_chain(xfers, pri=10)

            # Verify all destinations
            for i in range(4):
                expected = [i * 10 + j for j in range(4)]
                result = self.fixture.read_memory(0x5000 + i * 0x1000, 4)
                assert result == expected, f"Transfer {i} mismatch"

            print("  Multiple memcpy_chain test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# devcpy Tests
# =============================================================================

def test_devcpy_basic():
    """Test basic devcpy operation with request synchronization."""
    print("\n=== Test: Basic devcpy ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize source memory
            data = [0xAA, 0xBB, 0xCC, 0xDD]
            self.fixture.init_memory(0x1000, data)

            async def device_requests():
                """Simulate device requesting chunks."""
                await self.wait(zdc.Time.ns(10))
                for _ in range(4):  # 4 chunks of 1 access each
                    await self.fixture.dma.req_transfer(42)
                    await self.wait(zdc.Time.ns(10))

            async def dma_transfer():
                await self.fixture.dma.devcpy(
                    src=0x1000,
                    dst=0x2000,
                    sz=32,  # 4 * 8 bytes
                    acc_sz=8,
                    chk_sz=1,  # 1 access per chunk
                    inc_src=True,
                    inc_dst=True,
                    req_id=42
                )

            # Run device and DMA concurrently with simulation driver
            await asyncio.gather(device_requests(), dma_transfer())

            # Verify destination
            result = self.fixture.read_memory(0x2000, 4)
            assert result == data, f"Data mismatch: {result} != {data}"

            print("  Basic devcpy test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_devcpy_no_increment():
    """Test devcpy with no address increment (FIFO-style)."""
    print("\n=== Test: devcpy no increment ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize single source word
            self.fixture.mem.storage[0x1000] = 0x55

            async def device_requests():
                await self.wait(zdc.Time.ns(10))
                for _ in range(4):
                    await self.fixture.dma.req_transfer(99)
                    await self.wait(zdc.Time.ns(10))

            async def dma_transfer():
                await self.fixture.dma.devcpy(
                    src=0x1000,
                    dst=0x2000,
                    sz=32,
                    acc_sz=8,
                    chk_sz=1,
                    inc_src=False,  # Don't increment source
                    inc_dst=True,
                    req_id=99
                )

            await asyncio.gather(device_requests(), dma_transfer())

            # All 4 words should have same value (read from same address)
            result = self.fixture.read_memory(0x2000, 4)
            assert result == [0x55, 0x55, 0x55, 0x55], f"Data mismatch: {result}"

            print("  devcpy no increment test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_devcpy_multi_access_chunk():
    """Test devcpy with multiple accesses per chunk."""
    print("\n=== Test: devcpy multi-access chunk ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            data = [0x10, 0x20, 0x30, 0x40]
            self.fixture.init_memory(0x1000, data)

            async def device_requests():
                await self.wait(zdc.Time.ns(10))
                # Only 2 requests needed (2 accesses per chunk, 4 total)
                for _ in range(2):
                    await self.fixture.dma.req_transfer(77)
                    await self.wait(zdc.Time.ns(10))

            async def dma_transfer():
                await self.fixture.dma.devcpy(
                    src=0x1000,
                    dst=0x2000,
                    sz=32,
                    acc_sz=8,
                    chk_sz=2,  # 2 accesses per chunk
                    inc_src=True,
                    inc_dst=True,
                    req_id=77
                )

            await asyncio.gather(device_requests(), dma_transfer())

            result = self.fixture.read_memory(0x2000, 4)
            assert result == data, f"Data mismatch: {result} != {data}"

            print("  devcpy multi-access chunk test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# devcpy_chain Tests
# =============================================================================

def test_devcpy_chain_basic():
    """Test basic devcpy_chain operation."""
    print("\n=== Test: Basic devcpy_chain ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize two source regions
            data1 = [0x11, 0x22]
            data2 = [0x33, 0x44]
            self.fixture.init_memory(0x1000, data1)
            self.fixture.init_memory(0x3000, data2)

            async def device_requests():
                await self.wait(zdc.Time.ns(10))
                # 4 requests total (2 per transfer, 1 access per chunk)
                for _ in range(4):
                    await self.fixture.dma.req_transfer(88)
                    await self.wait(zdc.Time.ns(10))

            async def dma_transfer():
                xfers = [
                    DevCpyTest(src=0x1000, dst=0x2000, sz=16, acc_sz=8, chk_sz=1,
                           inc_src=True, inc_dst=True),
                    DevCpyTest(src=0x3000, dst=0x4000, sz=16, acc_sz=8, chk_sz=1,
                           inc_src=True, inc_dst=True)
                ]
                await self.fixture.dma.devcpy_chain(xfers, req_id=88)

            await asyncio.gather(device_requests(), dma_transfer())

            result1 = self.fixture.read_memory(0x2000, 2)
            result2 = self.fixture.read_memory(0x4000, 2)
            assert result1 == data1, f"First transfer mismatch: {result1}"
            assert result2 == data2, f"Second transfer mismatch: {result2}"

            print("  Basic devcpy_chain test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# ReqOp Interface Tests
# =============================================================================

def test_req_transfer_unknown_id():
    """Test req_transfer with unknown ID does nothing."""
    print("\n=== Test: req_transfer unknown ID ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Should not raise an error
            await self.fixture.dma.req_transfer(999)
            print("  req_transfer unknown ID test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_multiple_concurrent_req_ids():
    """Test multiple concurrent transfers with different req_ids."""
    print("\n=== Test: Multiple concurrent req_ids ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize source regions
            data1 = [0xA1, 0xA2]
            data2 = [0xB1, 0xB2]
            self.fixture.init_memory(0x1000, data1)
            self.fixture.init_memory(0x3000, data2)

            async def device_requests_1():
                await self.wait(zdc.Time.ns(10))
                for _ in range(2):
                    await self.fixture.dma.req_transfer(100)
                    await self.wait(zdc.Time.ns(20))

            async def device_requests_2():
                await self.wait(zdc.Time.ns(15))
                for _ in range(2):
                    await self.fixture.dma.req_transfer(200)
                    await self.wait(zdc.Time.ns(20))

            async def dma_transfer_1():
                await self.fixture.dma.devcpy(
                    src=0x1000, dst=0x2000, sz=16, acc_sz=8, chk_sz=1,
                    inc_src=True, inc_dst=True, req_id=100
                )

            async def dma_transfer_2():
                await self.fixture.dma.devcpy(
                    src=0x3000, dst=0x4000, sz=16, acc_sz=8, chk_sz=1,
                    inc_src=True, inc_dst=True, req_id=200
                )

            await asyncio.gather(
                device_requests_1(), device_requests_2(),
                dma_transfer_1(), dma_transfer_2()
            )

            result1 = self.fixture.read_memory(0x2000, 2)
            result2 = self.fixture.read_memory(0x4000, 2)
            assert result1 == data1, f"Transfer 1 mismatch: {result1}"
            assert result2 == data2, f"Transfer 2 mismatch: {result2}"

            print("  Multiple concurrent req_ids test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# Memory Lock Tests
# =============================================================================

def test_concurrent_memcpy():
    """Test concurrent memcpy operations share memory lock."""
    print("\n=== Test: Concurrent memcpy ===")

    @zdc.dataclass
    class Top(zdc.Component):
        fixture: DmaTestFixture = zdc.field()

        async def run(self):
            # Initialize two source regions
            data1 = list(range(8))
            data2 = list(range(100, 108))
            self.fixture.init_memory(0x1000, data1)
            self.fixture.init_memory(0x3000, data2)

            # Run two memcpy operations concurrently
            await asyncio.gather(
                self.fixture.dma.memcpy(src=0x1000, dst=0x2000, sz=64),
                self.fixture.dma.memcpy(src=0x3000, dst=0x4000, sz=64)
            )

            # Both should complete successfully
            result1 = self.fixture.read_memory(0x2000, 8)
            result2 = self.fixture.read_memory(0x4000, 8)
            assert result1 == data1, f"Transfer 1 mismatch: {result1}"
            assert result2 == data2, f"Transfer 2 mismatch: {result2}"

            print("  Concurrent memcpy test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


def test_memcpy_with_delay():
    """Test memcpy with memory access delays."""
    print("\n=== Test: memcpy with delay ===")

    @zdc.dataclass
    class Top(zdc.Component):
        mem: MockMemory = zdc.field()
        dma: DmaOpOpAlg = zdc.field()

        def __bind__(self):
            return {self.dma.mem: self.mem}

        async def run(self):
            # Set delays
            self.mem.read_delay = zdc.Time.ns(10)
            self.mem.write_delay = zdc.Time.ns(10)

            # Initialize source data (4 words, 8-byte aligned)
            for i in range(4):
                addr = 0x1000 + i * 8
                for b in range(8):
                    self.mem.storage[addr + b] = ((0x10 + i) >> (b * 8)) & 0xFF

            start_time = self.time()

            # Copy 32 bytes (4 accesses of 8 bytes each)
            await self.dma.memcpy(src=0x1000, dst=0x2000, sz=32)

            end_time = self.time()

            # Verify data was copied
            for i in range(4):
                src_addr = 0x1000 + i * 8
                dst_addr = 0x2000 + i * 8
                for b in range(8):
                    expected = self.mem.storage.get(src_addr + b, 0)
                    actual = self.mem.storage.get(dst_addr + b, 0)
                    assert actual == expected, f"Byte mismatch at offset {i*8+b}"

            # Check timing: 4 reads + 4 writes = 8 accesses * 10ns = 80ns
            elapsed_ns = (end_time.as_ns() - start_time.as_ns())
            print(f"  Elapsed time: {elapsed_ns} ns")
            assert elapsed_ns >= 80, f"Expected >= 80ns, got {elapsed_ns}ns"

            print("  memcpy with delay test PASSED")

    t = Top()
    asyncio.run(t.run())
    t.shutdown()


# =============================================================================
# Main Test Runner
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DmaOpOpAlg Unit Tests")
    print("=" * 60)

    # Structure tests
    test_dma_implements_interfaces()
    test_dma_has_memory_port()

    # memcpy tests
    test_memcpy_basic()
    test_memcpy_with_priority()
    test_memcpy_large_transfer()
    test_memcpy_unaligned()

    # memcpy_chain tests
    test_memcpy_chain_basic()
    test_memcpy_chain_multiple()

    # devcpy tests
    test_devcpy_basic()
    test_devcpy_no_increment()
    test_devcpy_multi_access_chunk()

    # devcpy_chain tests
    test_devcpy_chain_basic()

    # ReqOp tests
    test_req_transfer_unknown_id()
    test_multiple_concurrent_req_ids()

    # Memory lock tests
    test_concurrent_memcpy()

    # Timing tests
    test_memcpy_with_delay()

    print("\n" + "=" * 60)
    print("All DmaOpOpAlg tests PASSED!")
    print("=" * 60)
