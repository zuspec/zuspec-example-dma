# Project Dependencies - Quick Start Guide

This README provides quick access to dependency information for the zuspec-example-dma project.

## Quick Links

- 📋 **Full Dependency Catalog**: See [DEPENDENCIES.md](DEPENDENCIES.md) for complete dependency information
- 🔍 **Check svdep Status**: Run `python check_svdep.py` to check if svdep is installed

## What is svdep?

**svdep** is a SystemVerilog dependency management tool that:
- Tracks dependencies between SystemVerilog files
- Enables incremental compilation (only recompile what changed)
- Works with tools like zuspec that generate SystemVerilog code

**Important**: svdep is **NOT** automatically installed with zuspec or this project. It is an optional tool that you can install if you need SystemVerilog dependency tracking.

## Quick Checks

### Check if svdep is installed

```bash
# Run the checker script
python check_svdep.py

# Or manually check
python -c "import svdep; print('svdep is installed')" 2>/dev/null || echo "svdep is NOT installed"
```

### Install svdep (if needed)

```bash
# Install in your system Python
pip install svdep

# Or install in the IVPM virtual environment
./packages/python/bin/pip install svdep
```

### Verify installation

```bash
# Check version
python -c "import svdep; print(f'svdep version: {svdep.__version__}')"

# Or use pip
pip show svdep
```

## Project Dependencies Overview

This project uses:
1. **IVPM** - Package manager for dependency management
2. **Zuspec** - Hardware modeling framework
3. **Sphinx** - Documentation generation
4. **MyST Parser** - Markdown support for docs
5. **Mermaid** - Diagram generation in docs

### Installing Project Dependencies

```bash
# Install ivpm (if not installed)
pip install ivpm

# Install all project dependencies
ivpm update

# Check installation
./packages/python/bin/pip list
```

## Directory Structure

```
zuspec-example-dma/
├── ivpm.yaml              # Dependency definitions
├── DEPENDENCIES.md        # Complete dependency catalog
├── check_svdep.py         # Script to check svdep status
├── README_DEPENDENCIES.md # This file
├── packages/              # IVPM-managed dependencies
│   └── python/            # Python virtual environment
│       ├── bin/           # Python executables
│       └── lib/           # Python packages
└── docs/                  # Documentation
    └── spec/              # Specification documents
```

## Common Commands

```bash
# Check svdep status
python check_svdep.py

# Update all dependencies
ivpm update

# Force reinstall Python packages
ivpm update --force-py-install

# Sync with upstream repositories
ivpm sync

# Activate IVPM environment
ivpm activate

# List installed packages
./packages/python/bin/pip list

# Build documentation
./packages/python/bin/sphinx-build -b html docs/spec docs/spec/_build/html
```

## Troubleshooting

### svdep not found
- svdep is not included by default - install it manually if needed:
  ```bash
  pip install svdep
  ```

### IVPM packages directory doesn't exist
- Run `ivpm update` to create the environment and install dependencies

### Import errors for zuspec
- Ensure dependencies are installed: `ivpm update`
- Use the IVPM Python: `./packages/python/bin/python`

## More Information

- Full dependency list and details: [DEPENDENCIES.md](DEPENDENCIES.md)
- Zuspec documentation: https://zuspec.github.io/
- svdep repository: https://github.com/fvutils/svdep
- IVPM documentation: https://github.com/fvutils/ivpm

## Summary

✅ **Dependencies Cataloged**: All project dependencies are documented in DEPENDENCIES.md

✅ **svdep Status**: svdep is an **optional** tool, not included by default. Use `check_svdep.py` to check its status.

✅ **Dependency Management**: Use IVPM (`ivpm update`) to manage project dependencies

For the complete dependency catalog with version information and detailed descriptions, see [DEPENDENCIES.md](DEPENDENCIES.md).
