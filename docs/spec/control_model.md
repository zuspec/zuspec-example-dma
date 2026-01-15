# Programmatic Control Model

## Control Interface

The DMA engine is controlled through a memory-mapped register interface. Software interacts with the DMA by reading and writing to control and status registers.

## Register Organization

Registers are organized per-channel with a common control block:

```{mermaid}
graph TB
    subgraph "DMA Register Space"
        Global[Global Control Registers]
        CH0[Channel 0 Registers]
        CH1[Channel 1 Registers]
        CH2[Channel 2 Registers]
        CH3[Channel 3 Registers]
    end
    
    subgraph "Channel Register Block"
        SRC[Source Address]
        DST[Destination Address]
        SIZE[Transfer Size]
        CTRL[Control Register]
        STAT[Status Register]
    end
    
    Global -.-> CH0
    CH0 -.-> SRC
    CH0 -.-> DST
    CH0 -.-> SIZE
    CH0 -.-> CTRL
    CH0 -.-> STAT
    
    style Global fill:#ffe1e1
    style CH0 fill:#e1f5ff
    style CH1 fill:#e1f5ff
    style CH2 fill:#e1f5ff
    style CH3 fill:#e1f5ff
```

## Register Types

### Per-Channel Configuration Registers

**Source Address Register (CHn_SRC_ADDR)**
- Width: Address bus width
- Access: Read/Write
- Purpose: Specifies the starting address for read operations
- Constraints: Must be aligned to transfer unit boundary

**Destination Address Register (CHn_DST_ADDR)**
- Width: Address bus width
- Access: Read/Write
- Purpose: Specifies the starting address for write operations
- Constraints: Must be aligned to transfer unit boundary

**Transfer Size Register (CHn_XFER_SIZE)**
- Width: Sufficient to address maximum transfer
- Access: Read/Write
- Purpose: Specifies the number of units to transfer
- Constraints: Must be non-zero, within maximum transfer limit

### Per-Channel Control Register (CHn_CTRL)

Bit fields controlling channel operation:

| Bit(s) | Name | Access | Description |
|--------|------|--------|-------------|
| 0 | ENABLE | RW | Enable channel operation |
| 1 | START | W | Trigger programmatic transfer (self-clearing) |
| 2 | RESET | W | Reset channel to idle state (self-clearing) |
| 3 | TRIG_MODE | RW | 0=Programmatic, 1=Peripheral trigger |
| [7:4] | TRIG_SEL | RW | Peripheral trigger source selection (when TRIG_MODE=1) |
| 8 | INT_EN | RW | Enable transfer complete interrupt |
| 9 | ERR_INT_EN | RW | Enable error interrupt |
| [31:10] | RESERVED | RO | Reserved for future use |

### Per-Channel Status Register (CHn_STATUS)

Bit fields reporting channel status:

| Bit(s) | Name | Access | Description |
|--------|------|--------|-------------|
| 0 | IDLE | RO | Channel is idle |
| 1 | ACTIVE | RO | Transfer in progress |
| 2 | COMPLETE | RC | Transfer completed (read to clear) |
| 3 | ERROR | RC | Error occurred (read to clear) |
| [7:4] | ERR_CODE | RO | Error code (valid when ERROR=1) |
| [31:8] | RESERVED | RO | Reserved |

Error codes:
- 0: No error
- 1: Invalid source address
- 2: Invalid destination address
- 3: Alignment error
- 4: Invalid size
- 5-15: Reserved

### Global Control Registers

**Global Enable Register (DMA_GLOBAL_EN)**
- Bit 0: Master enable for entire DMA engine
- Must be set for any channel to operate

**Interrupt Status Register (DMA_INT_STATUS)**
- Read-only register showing pending interrupts from all channels
- Bit n: Channel n interrupt pending

## Control Sequences

### Programmatic Transfer Sequence

```{mermaid}
sequenceDiagram
    participant SW as Software
    participant REG as DMA Registers
    participant ENG as DMA Engine
    
    SW->>REG: Write CHn_SRC_ADDR
    SW->>REG: Write CHn_DST_ADDR
    SW->>REG: Write CHn_XFER_SIZE
    SW->>REG: Write CHn_CTRL.ENABLE = 1
    SW->>REG: Write CHn_CTRL.START = 1
    
    activate ENG
    Note over ENG: Transfer in progress
    ENG->>REG: Set CHn_STATUS.ACTIVE
    
    Note over ENG: Data transfer
    
    ENG->>REG: Clear CHn_STATUS.ACTIVE
    ENG->>REG: Set CHn_STATUS.COMPLETE
    deactivate ENG
    
    SW->>REG: Read CHn_STATUS (clears COMPLETE)
```

### Peripheral-Triggered Transfer Sequence

```{mermaid}
sequenceDiagram
    participant SW as Software
    participant REG as DMA Registers
    participant ENG as DMA Engine
    participant PER as Peripheral
    
    SW->>REG: Write CHn_SRC_ADDR
    SW->>REG: Write CHn_DST_ADDR
    SW->>REG: Write CHn_XFER_SIZE
    SW->>REG: Write CHn_CTRL.TRIG_MODE = 1
    SW->>REG: Write CHn_CTRL.TRIG_SEL = X
    SW->>REG: Write CHn_CTRL.ENABLE = 1
    
    Note over ENG: Waiting for trigger
    
    PER->>ENG: Trigger Signal
    
    activate ENG
    ENG->>REG: Set CHn_STATUS.ACTIVE
    Note over ENG: Data transfer
    ENG->>REG: Clear CHn_STATUS.ACTIVE
    ENG->>REG: Set CHn_STATUS.COMPLETE
    deactivate ENG
```

### Error Handling Sequence

```{mermaid}
sequenceDiagram
    participant SW as Software
    participant REG as DMA Registers
    participant ENG as DMA Engine
    
    SW->>REG: Write invalid configuration
    SW->>REG: Write CHn_CTRL.START = 1
    
    ENG->>REG: Set CHn_STATUS.ERROR
    ENG->>REG: Set CHn_STATUS.ERR_CODE
    
    Note over SW: Interrupt received (if enabled)
    
    SW->>REG: Read CHn_STATUS
    Note over SW: Check ERROR and ERR_CODE
    SW->>REG: Write CHn_CTRL.RESET = 1
    ENG->>REG: Clear CHn_STATUS.ERROR
    ENG->>REG: Set CHn_STATUS.IDLE
```

## Interrupt Model

The DMA engine supports interrupt-driven operation:

### Interrupt Sources

Each channel can generate interrupts for:
1. **Transfer Complete**: Normal transfer completion
2. **Error**: Error condition detected

### Interrupt Configuration

- Per-channel interrupt enable bits in CHn_CTRL register
- Global interrupt status in DMA_INT_STATUS register
- Interrupts are level-sensitive, remain asserted until cleared

### Interrupt Service Flow

```{mermaid}
graph TB
    INT[Interrupt Received] --> READ[Read DMA_INT_STATUS]
    READ --> IDENTIFY[Identify Channels]
    IDENTIFY --> STATUS[Read CHn_STATUS]
    STATUS --> COMPLETE{Transfer Complete?}
    COMPLETE -->|Yes| PROC_COMP[Process Completion]
    COMPLETE -->|No| ERROR{Error?}
    ERROR -->|Yes| PROC_ERR[Handle Error]
    ERROR -->|No| OTHER[Other Processing]
    PROC_COMP --> CLEAR[Read STATUS to Clear]
    PROC_ERR --> CLEAR
    OTHER --> CLEAR
    CLEAR --> DONE[Return from ISR]
```

## Configuration Constraints

### Timing Constraints

- Configuration registers must not be modified while channel is active
- Changes to configuration take effect when channel is enabled
- Channel must be disabled before reconfiguration

### Address Constraints

- Source and destination addresses must be within valid memory regions
- Addresses must be aligned to transfer unit size
- Source and destination ranges should not overlap (undefined behavior)

### Size Constraints

- Transfer size must be greater than zero
- Transfer size must not exceed implementation-defined maximum
- Total transfer must not cross memory region boundaries

## Atomic Operations

### Read-Modify-Write Safety

When multiple software contexts access DMA registers:
- Each channel's registers are independent
- Global registers may require atomic read-modify-write operations
- Status register reads that clear flags are atomic

### Recommended Software Practices

1. Use exclusive access primitives for control register updates
2. Disable interrupts during critical configuration sequences
3. Verify idle state before reconfiguring channels
4. Clear status flags after reading to prevent spurious interrupts
