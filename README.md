# Zuspec DMA Example

This repository contains a high-level specification for a DMA (Direct Memory Access) engine using the Zuspec framework.

## Documentation

The specification documentation is located in `docs/spec/` and includes:

- System overview and architecture
- Operation types and sequences
- Control model and register interface
- Design assumptions and constraints

To build the documentation:

```bash
# Install dependencies first
ivpm update

# Build HTML documentation
./packages/python/bin/sphinx-build -b html docs/spec docs/spec/_build/html

# Or use the Makefile
cd docs/spec && make html
```

## Project Dependencies

📋 **See [DEPENDENCIES.md](DEPENDENCIES.md)** for a complete catalog of project dependencies.

🔍 **Check svdep Status**: Run `python check_svdep.py` to check if the svdep SystemVerilog dependency manager is installed.

Quick reference: [README_DEPENDENCIES.md](README_DEPENDENCIES.md)

### Quick Start

```bash
# Install IVPM package manager
pip install ivpm

# Install project dependencies
ivpm update

# Check svdep status (optional SystemVerilog dependency manager)
python check_svdep.py

# Build documentation
./packages/python/bin/sphinx-build -b html docs/spec docs/spec/_build/html
```

## Repository Structure

```
zuspec-example-dma/
├── docs/spec/           # Specification documentation
│   ├── overview.md      # System overview
│   ├── operations.md    # Transfer operations
│   ├── control_model.md # Register and control interface
│   └── assumptions.md   # Design assumptions
├── ivpm.yaml            # Dependency configuration
├── DEPENDENCIES.md      # Complete dependency catalog
├── check_svdep.py       # Script to check svdep installation
└── README.md            # This file
```

## Dependencies

This project uses:

- **Zuspec**: Hardware modeling and specification framework
- **Sphinx**: Documentation generation
- **MyST Parser**: Markdown support for Sphinx
- **Mermaid**: Diagram generation
- **svdep** (optional): SystemVerilog dependency management tool

For detailed dependency information, see [DEPENDENCIES.md](DEPENDENCIES.md).

## About Zuspec

Zuspec is a Python-based, multi-abstraction framework for hardware modeling. It provides:
- Unified modeling language for hardware design
- Multiple backend targets (SystemVerilog, C++, etc.)
- Integration with verification and synthesis flows

Learn more at [zuspec.github.io](https://zuspec.github.io/)

## About svdep

svdep is a SystemVerilog dependency management tool that can be used alongside zuspec to track dependencies in generated SystemVerilog files. 

**Note**: svdep is **not** automatically installed with this project. It is an optional tool that you can install if needed for SystemVerilog dependency tracking.

Check if svdep is installed:
```bash
python check_svdep.py
```

Install svdep if needed:
```bash
pip install svdep
# Or in IVPM environment:
./packages/python/bin/pip install svdep
```

## License

See [LICENSE](LICENSE) file for details.
