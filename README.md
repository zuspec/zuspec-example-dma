# Zuspec Example: DMA

This project provides an example of a DMA engine designed with Zuspec.

## Quickstart

### Installing Dependencies

Zuspec uses [IVPM]() to fetch dependencies and create a project-local 
Python virtual environment. You can install dependencies as follows:

```bash
% ivpm update
```

Or, use the convenience script `bootstrap.sh`.

### Environment Configuration

Zuspec uses [direnv]() to manage the environment. If you install
`direnv`, simply run:

```bash
% direnv allow
```

Currently, the key requirement for these examples is to have 
`packages/python/bin` in your PATH. You can manually add this if
you choose not to use `direnv`:

```bash
% export PATH=$(pwd)/packages/python/bin:${PATH}
```

### Running Unit Tests

Unit tests are implemented with [pytest](). Run them as follows:

```bash
% pytest -s tests/unit
```




