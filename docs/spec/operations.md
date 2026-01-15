# DMA Operations

## Transfer Operation Types

The DMA engine supports two fundamental transfer operation modes, distinguished by their initiation mechanism.

### Programmatic Transfer

Software-initiated transfers where the CPU configures and triggers the DMA operation.

```{mermaid}
sequenceDiagram
    participant CPU
    participant DMA
    participant Memory
    
    CPU->>DMA: Configure Channel (src, dst, size)
    CPU->>DMA: Start Transfer
    activate DMA
    loop Transfer Loop
        DMA->>Memory: Read from source
        Memory-->>DMA: Data
        DMA->>Memory: Write to destination
    end
    DMA->>CPU: Transfer Complete (interrupt)
    deactivate DMA
```

**Key Characteristics**:
- CPU explicitly initiates the transfer
- Transfer begins immediately after start command
- Useful for bulk data operations under software control
- Deterministic start time

### Peripheral-Triggered Transfer

Hardware-initiated transfers where peripheral devices trigger pre-configured DMA operations.

```{mermaid}
sequenceDiagram
    participant CPU
    participant DMA
    participant Peripheral
    participant Memory
    
    CPU->>DMA: Configure Channel (src, dst, size)
    CPU->>DMA: Enable Peripheral Trigger
    Note over DMA: DMA waits for trigger
    Peripheral->>DMA: Trigger Signal
    activate DMA
    loop Transfer Loop
        DMA->>Memory: Read from source
        Memory-->>DMA: Data
        DMA->>Memory: Write to destination
    end
    DMA->>CPU: Transfer Complete (interrupt)
    deactivate DMA
```

**Key Characteristics**:
- Peripheral device initiates the transfer
- DMA channel must be pre-configured and armed
- Supports event-driven data movement
- Minimal latency from trigger to transfer start

## Transfer Phases

Every DMA transfer operation proceeds through distinct phases:

```{mermaid}
stateDiagram-v2
    [*] --> Idle
    Idle --> Configuration: CPU configures channel
    Configuration --> Armed: Enable trigger/Start
    Armed --> Active: Trigger received
    Active --> Active: Data transfer in progress
    Active --> Complete: Transfer finished
    Complete --> Idle: Reset/Acknowledge
    
    note right of Configuration
        Set source address
        Set destination address
        Set transfer size
    end note
    
    note right of Active
        Read from source
        Write to destination
        Update counters
    end note
```

### 1. Configuration Phase

The channel is configured with transfer parameters:
- **Source Address**: Starting address for read operations
- **Destination Address**: Starting address for write operations
- **Transfer Size**: Number of bytes/words to transfer
- **Trigger Mode**: Programmatic or peripheral trigger selection

### 2. Armed Phase

The channel is prepared for transfer:
- For programmatic mode: immediately proceeds to Active
- For peripheral mode: waits for external trigger signal

### 3. Active Phase

The actual data transfer occurs:
- Sequential read operations from source address
- Sequential write operations to destination address
- Internal counters track progress
- Address pointers increment with each operation

### 4. Complete Phase

Transfer finishes and status is reported:
- Transfer complete flag is set
- Optional interrupt generated to CPU
- Channel returns to idle state

## Transfer Granularity

### Transfer Unit

Each DMA operation transfers data in units (typically word-sized):
- Single unit per memory access
- Source and destination must be properly aligned
- Transfer size specified in number of units

### Burst Considerations

While the basic operation is unit-based, implementations may optimize with burst transfers:
- Multiple units transferred in a single bus transaction
- Reduces bus overhead
- Maintains semantic equivalence to unit-by-unit transfer

## Concurrent Operations

Multiple channels can operate simultaneously:

```{mermaid}
gantt
    title Multi-Channel Concurrent Operation
    dateFormat X
    axisFormat %L
    
    section Channel 0
    Transfer A :a0, 0, 100
    
    section Channel 1
    Idle :i1, 0, 20
    Transfer B :a1, 20, 80
    
    section Channel 2
    Transfer C :a2, 0, 150
    
    section Channel 3
    Idle :i3, 0, 50
    Transfer D :a3, 50, 100
```

**Concurrency Rules**:
- Each channel operates independently
- No resource conflicts between channels
- Memory system handles concurrent access arbitration
- Transfer completion is independent per channel

## Error Conditions

The DMA engine detects and reports several error conditions:

1. **Invalid Address**: Source or destination address outside valid memory range
2. **Alignment Error**: Address not aligned to transfer unit boundary
3. **Channel Busy**: Attempt to configure an active channel
4. **Trigger Timeout**: Peripheral trigger expected but not received (implementation-specific)

Error handling:
- Transfer is aborted on error detection
- Error status flag set for the channel
- Optional error interrupt generated
- Channel requires reset before reuse
