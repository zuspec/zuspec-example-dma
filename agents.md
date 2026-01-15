# Project Initialization and Dependencies

This document describes how to initialize the zuspec-example-dma project and catalogs its dependencies.

## Prerequisites

- Python 3.12 or later
- pip package manager
- Git

## Initialization Steps

### 1. Install IVPM (IP and Verification Package Manager)

```bash
pip install ivpm
```

IVPM is a Python- and Git-centric utility for managing project dependencies in hardware design and verification environments.

### 2. Initialize the Project

From the repository root directory, run:

```bash
ivpm update
```

This command will:
- Create a Python virtual environment in `packages/python/`
- Fetch all source dependencies specified in `ivpm.yaml`
- Install all specified Python package dependencies

### 3. Activate the Virtual Environment

After initialization, activate the virtual environment:

```bash
source packages/python/bin/activate
```

## Project Dependencies

### Dependency Management Configuration

The project uses `ivpm.yaml` to define its dependencies. The configuration includes:

**Package Name:** zuspec-example-dma

**Dependency Set:** default-dev

### Python Dependencies (from PyPI)

The following Python packages are required for documentation generation:

1. **sphinx** - Documentation generation framework
   - Source: PyPI
   - Purpose: Generate HTML documentation from reStructuredText and Markdown sources

2. **sphinxcontrib-mermaid** - Mermaid diagram support for Sphinx
   - Source: PyPI
   - Purpose: Enable Mermaid diagram rendering in Sphinx documentation

3. **myst-parser** - Markdown parser for Sphinx
   - Source: PyPI
   - Purpose: Allow MyST (Markedly Structured Text) Markdown in Sphinx documentation

### Git-based Dependencies

4. **zuspec** - Zuspec verification framework
   - Source: https://github.com/zuspec/zuspec.git
   - Purpose: Core verification framework for the DMA example
   - Note: This is a git repository dependency that will be cloned during `ivpm update`

### Implicitly Installed Dependencies

When running `ivpm update`, the following are also installed:

- **ivpm** - The package manager itself
- Various transitive dependencies required by Sphinx, MyST Parser, and other packages

## SystemVerilog Dependency Management (svdep)

### Status: NOT LOADED

**svdep** is a SystemVerilog dependency-management tool that helps determine when SystemVerilog files have been modified.

#### Current Status in Project

- **Installation Status:** NOT INSTALLED
- **Configuration:** Not included in `ivpm.yaml` dependencies
- **Availability:** Not available in the project virtual environment

#### About svdep

- **Purpose:** Tracks SystemVerilog file dependencies and changes
- **Installation:** `pip install svdep`
- **Source:** https://github.com/fvutils/svdep
- **Use Case:** Optimize build times by detecting when recompilation is necessary

#### Why svdep is Not Included

This project focuses on high-level specification and documentation using Sphinx/Mermaid/MyST. Since there are no SystemVerilog source files in the current repository structure, svdep is not needed as a dependency.

If SystemVerilog development is added to this project in the future, svdep should be added to the `ivpm.yaml` dependencies:

```yaml
deps:
  - name: svdep
    src: pypi
```

## Verification

After initialization, verify the setup:

```bash
# Activate environment
source packages/python/bin/activate

# Check installed packages
pip list

# Verify key tools are available
sphinx-build --version
python -c "import myst_parser"
python -c "import sphinxcontrib.mermaid"
```

## Building Documentation

To build the HTML documentation:

```bash
source packages/python/bin/activate
cd docs/spec
make html
```

The built documentation will be available in `docs/spec/_build/html/`.

## Troubleshooting

### Git SSH Authentication Issues

If `ivpm update` fails with Git SSH errors, ensure:
1. Git is configured with appropriate credentials
2. SSH keys are set up for GitHub if using SSH URLs
3. HTTPS URLs are properly configured in `ivpm.yaml`

### Missing Dependencies

If packages are missing after `ivpm update`:
1. Ensure you've activated the virtual environment: `source packages/python/bin/activate`
2. Try updating again: `ivpm update`
3. Manually install missing packages: `pip install <package-name>`

## Summary

- **Initialization Tool:** IVPM (IP and Verification Package Manager)
- **Primary Dependencies:** sphinx, sphinxcontrib-mermaid, myst-parser, zuspec
- **Virtual Environment Location:** `packages/python/`
- **svdep Status:** Not loaded, not required for current project scope
- **Primary Use Case:** Documentation generation and verification framework development
