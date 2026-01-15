# Zuspec DMA Specification

This directory contains the high-level specification for the Zuspec DMA engine.

## Building the Documentation

To build the HTML documentation:

```bash
# From the repository root
packages/python/bin/sphinx-build -b html docs/spec docs/spec/_build/html
```

Or use the Makefile:

```bash
cd docs/spec
make html
```

## Specification Structure

The specification is organized into four main sections:

### 1. Overview (`overview.md`)
- System introduction and context
- Key features
- Channel organization
- Design philosophy
- **Diagrams**: System context diagram, channel organization

### 2. Operations (`operations.md`)
- Transfer operation types (programmatic and peripheral-triggered)
- Transfer phases and state machine
- Transfer granularity and semantics
- Concurrent operations
- Error conditions
- **Diagrams**: Sequence diagrams for both transfer types, state machine, concurrent operation timeline

### 3. Control Model (`control_model.md`)
- Register-based control interface
- Register organization and types
- Control sequences for different operations
- Interrupt model
- Configuration constraints
- **Diagrams**: Register organization, control sequences, interrupt service flow

### 4. Assumptions (`assumptions.md`)
- System assumptions (memory, data model, bus model)
- Operational assumptions
- Error handling assumptions
- Software responsibilities
- Performance considerations
- Explicit exclusions

## Technologies Used

- **Sphinx**: Documentation generation
- **MyST Parser**: Markdown support for Sphinx
- **Mermaid**: Diagram generation (sequence, state, flowchart, gantt)

## Key Characteristics

This specification focuses on:
- **High-level behavior**: What the DMA does, not how it's implemented
- **Interface contracts**: Clear expectations for software interaction
- **Operational semantics**: Transfer behavior and guarantees
- **Key assumptions**: Explicit constraints and responsibilities

The specification intentionally avoids architectural details, leaving implementation flexibility while ensuring functional clarity.
