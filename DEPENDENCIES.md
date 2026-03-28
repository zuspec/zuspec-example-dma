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
. packages/python/activate

# Or on Windows
packages\python\activate.bat
```

## Build and Documentation Commands

Based on the project structure:

```bash
# Build HTML documentation (from repository root)
cd docs/spec
make html

# Or using sphinx-build directly from repository root
sphinx-build -b html docs/spec docs/spec/_build/html

# Or from within docs/spec directory
cd docs/spec
sphinx-build -b html . _build/html
```

## Dependency Set Structure

The project uses a single dependency set:

- **default-dev**: Contains all dependencies needed for development and documentation building

## Future Considerations

As the project evolves, consider adding:
- **svdep** - If SystemVerilog source files are added
- **zuspec-be-sv** - If SystemVerilog backend generation is needed
- **Testing frameworks** - pytest or similar if automated tests are added
- **Code quality tools** - linters, formatters for any source code

## Last Updated

January 2026
