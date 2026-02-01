#!/bin/bash

uvx=$(which uvx)

if test ! -d packages; then
  if test ! -z $uvx; then
    $uvx ivpm update -d default
  else
    python -m venv packages/python
    ./packages/python/bin/pip install -U ivpm
    ./packages/python/bin/ivpm update -d default
  fi
fi
