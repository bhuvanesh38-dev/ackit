#!/bin/sh
# Works in any CI system: install, then validate. Exit code 1 fails the build.
set -e
pip install ackit
ackit validate "${ACKIT_BUNDLE:-context}" --strict
