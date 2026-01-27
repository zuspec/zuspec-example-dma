
# DMA: High-Level Requirements

The DMA engine supports fast memory transfer between two 
memory regions. It is intended for use with both storage
and memory-mapped I/O devices.

## Transfer Requirements: General
- Each transfer shall have an associated priority (0..15)
- Each transfer shall have non-overlapping source and destination addresses
- Each transfer shall specifies the total number of bytes to transfer

## Transfer Requirements: Device
In addition to the requirements above:
- Each transfer shall specify an access size (eg 1, 2, 4, 8)
- Each transfer shall specify a chunk size, denominated in <accesses>
- The total transfer size is in bytes, and must be a multiple of <access-size>
- The source and destination addresses shall be aligned to <access-size>
- Each transfer specifies whether the source/dest addresses are incremented
- Device I/O is generally controlled by requests from the device itself
  - Request a chunk -> DMA engine performs <chunk-size> <access-size> accesses

## Transfer Requirements: Chaining
- It shall be possible to specify lists of both general and device transfers

