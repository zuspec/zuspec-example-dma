# Project Dependencies

This document catalogs all dependencies used in the zuspec-example-dma project.

## Overview

This project uses [IVPM (IP and Verification Package Manager)](https://github.com/fvutils/ivpm) for dependency management. Dependencies are declared in the `ivpm.yaml` file at the root of the repository.

## Dependency Management Tool

- **IVPM**: IP and Verification Package Manager
  - Configuration file: `ivpm.yaml`
  - Purpose: Manages both Python packages and Git-based dependencies

## Current Dependencies

The project currently has the following dependencies defined in the `default-dev` dependency set:

### Documentation Dependencies

1. **sphinx**
   - Source: PyPI
   - Purpose: Documentation generation system
   - Used to build HTML documentation from reStructuredText and Markdown sources

2. **sphinxcontrib-mermaid**
   - Source: PyPI
   - Purpose: Mermaid diagram support for Sphinx
   - Enables rendering of sequence diagrams, state machines, flowcharts, and Gantt charts in documentation

3. **myst-parser**
   - Source: PyPI
   - Purpose: Markdown parser for Sphinx
   - Allows using Markdown (.md) files alongside reStructuredText in Sphinx projects
   - Supports extended Markdown features like colon fences, definition lists, and task lists

### Core Dependencies

4. **zuspec**
   - Source: Git repository
   - URL: https://github.com/zuspec/zuspec.git
   - Purpose: Core Zuspec framework for unified, multi-abstraction hardware modeling
   - Provides the foundation for Pythonic hardware design and verification

## SystemVerilog Dependency Management

### svdep Status: NOT LOADED

**svdep** is a SystemVerilog dependency management tool that is **not currently included** in this project's dependencies.

#### What is svdep?

- **Name**: svdep (SystemVerilog Dependency Manager)
- **Repository**: https://github.com/fvutils/svdep
- **PyPI**: https://pypi.org/project/svdep/
- **License**: Apache-2.0
- **Purpose**: Tracks dependencies between SystemVerilog files to determine when files have changed and need recompilation

#### Why svdep might be relevant

svdep could be useful for this project if:
- The project generates or works with SystemVerilog code
- There's a need to track SystemVerilog file dependencies
- Build optimization through dependency tracking is desired

#### Current assessment

Since this project is primarily a **documentation/specification project** for a DMA engine example, and does not currently contain SystemVerilog source files, **svdep is not required** at this time.

If the project expands to include:
- SystemVerilog implementation files
- Zuspec-to-SystemVerilog code generation (via zuspec-be-sv)
- SystemVerilog simulation or synthesis workflows

Then svdep could be added as a dependency by adding the following to `ivpm.yaml`:

```yaml
- name: svdep
  src: pypi
```

or

```yaml
- name: svdep
  url: https://github.com/fvutils/svdep.git
```

## Installing Dependencies

To install the project dependencies using IVPM:

```bash
# Install IVPM if not already installed
pip install ivpm

# Update dependencies defined in ivpm.yaml
ivpm update -a

# Activate the environment (bash/zsh)
source packages/python/activate.sh

# Or for fish shell
source packages/python/activate.fish
```

## Dependency Tree

```
zuspec-example-dma
├── sphinx (PyPI) - Documentation builder
├── sphinxcontrib-mermaid (PyPI) - Diagram support
├── myst-parser (PyPI) - Markdown parser
└── zuspec (Git) - Core framework
    └── [Additional transitive dependencies from zuspec]
```

## Development Setup

For a complete development setup:

1. Clone the repository
2. Install IVPM: `pip install ivpm`
3. Fetch dependencies: `ivpm update -a`
4. Activate environment: `source packages/python/activate.sh`
5. Build documentation: `cd docs/spec && make html`

## Notes

- All dependencies are for development and documentation purposes
- No runtime dependencies exist as this is a specification/example project
- Python 3.7+ is recommended for all tools
