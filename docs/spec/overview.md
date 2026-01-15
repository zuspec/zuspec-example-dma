# System Overview

## Introduction

The Zuspec DMA is a multi-channel Direct Memory Access (DMA) engine designed to transfer data between memory locations efficiently without CPU intervention. The system provides flexible transfer capabilities supporting both software-initiated and hardware-triggered operations.

## Key Features

- **Multi-Channel Architecture**: 4 independent DMA channels
- **Dual Trigger Modes**: Programmatic (software) and peripheral (hardware) triggers
- **Memory-to-Memory Transfers**: Efficient data movement between arbitrary memory locations
- **Concurrent Operations**: Multiple channels can operate simultaneously

## System Context

```{mermaid}
graph TB
    CPU[CPU/Processor] -->|Configure| DMA[DMA Engine]
    DMA -->|Read| SrcMem[Source Memory]
    SrcMem -->|Data| DMA
    DMA -->|Write| DstMem[Destination Memory]
    Peripherals[Peripheral Devices] -.->|Trigger| DMA
    DMA -->|Interrupt| CPU
    
    style DMA fill:#e1f5ff
    style CPU fill:#ffe1e1
    style Peripherals fill:#fff4e1
```

## Device Block Diagram

The following diagram shows the high-level structure of the DMA engine and its interfaces:

```{mermaid}
graph TB
    subgraph DMA_Engine["DMA Engine"]
        direction TB
        RegIF[Register Interface]
        
        subgraph Control["Control Block"]
            GlobalCtrl[Global Control]
            IntCtrl[Interrupt Controller]
        end
        
        subgraph Channels["Transfer Channels"]
            CH0[Channel 0<br/>Controller]
            CH1[Channel 1<br/>Controller]
            CH2[Channel 2<br/>Controller]
            CH3[Channel 3<br/>Controller]
        end
        
        TrigMux[Trigger<br/>Multiplexer]
        MemIF[Memory Interface]
        
        RegIF --> GlobalCtrl
        RegIF --> CH0
        RegIF --> CH1
        RegIF --> CH2
        RegIF --> CH3
        
        CH0 --> MemIF
        CH1 --> MemIF
        CH2 --> MemIF
        CH3 --> MemIF
        
        CH0 --> IntCtrl
        CH1 --> IntCtrl
        CH2 --> IntCtrl
        CH3 --> IntCtrl
        
        TrigMux --> CH0
        TrigMux --> CH1
        TrigMux --> CH2
        TrigMux --> CH3
    end
    
    CPU[CPU/Host] <-->|Register Bus| RegIF
    MemIF <-->|Memory Bus| Memory[Memory System]
    Periph[Peripheral Devices] -->|Trigger Signals| TrigMux
    IntCtrl -->|Interrupt| CPU
    
    style DMA_Engine fill:#e1f5ff
    style Control fill:#ffe1e1
    style Channels fill:#e1ffe1
    style RegIF fill:#fff4e1
    style MemIF fill:#fff4e1
```

### Interface Description

**Register Interface**
- Provides CPU access to configuration and status registers
- Supports read/write operations for channel configuration
- Bus protocol: Implementation-defined (e.g., APB, AXI-Lite)

**Memory Interface**
- Connects to system memory for data transfers
- Supports read and write operations
- Bus protocol: Implementation-defined (e.g., AXI, AHB)
- Arbitrates access between active channels

**Trigger Interface**
- Receives trigger signals from peripheral devices
- Multiplexes triggers to appropriate channels
- Edge-triggered inputs (implementation may include synchronization)

**Interrupt Output**
- Single interrupt line to CPU
- Aggregates interrupts from all channels
- Software reads interrupt status to identify source

## Channel Organization

The DMA engine consists of 4 independent channels (Channel 0-3), each capable of:

- Independent source and destination addressing
- Configurable transfer sizes
- Individual trigger configuration
- Separate status tracking

```{mermaid}
graph LR
    DMA[DMA Engine] --> CH0[Channel 0]
    DMA --> CH1[Channel 1]
    DMA --> CH2[Channel 2]
    DMA --> CH3[Channel 3]
    
    CH0 --> Mem[Memory System]
    CH1 --> Mem
    CH2 --> Mem
    CH3 --> Mem
    
    style DMA fill:#e1f5ff
    style CH0 fill:#e1ffe1
    style CH1 fill:#e1ffe1
    style CH2 fill:#e1ffe1
    style CH3 fill:#e1ffe1
```

## Design Philosophy

The DMA engine is designed around the following principles:

1. **Simplicity**: Clear, straightforward operation model
2. **Flexibility**: Support for diverse use cases through configuration
3. **Efficiency**: Minimize CPU involvement in data transfers
4. **Predictability**: Deterministic behavior for real-time applications
