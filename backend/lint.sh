#!/bin/bash
set -e

echo "=== Python Linting ==="
echo ""

echo "Running black..."
if black --check app/; then
  echo "[PASSED] black"
else
  echo "[FAILED] black"
  exit 1
fi

echo ""
echo "Running isort..."
if isort --check-only app/; then
  echo "[PASSED] isort"
else
  echo "[FAILED] isort"
  exit 1
fi

echo ""
echo "Running flake8..."
if flake8 app/; then
  echo "[PASSED] flake8"
else
  echo "[FAILED] flake8"
  exit 1
fi

echo ""
echo "Running mypy..."
if mypy app/; then
  echo "[PASSED] mypy"
else
  echo "[FAILED] mypy"
  exit 1
fi

echo ""
echo "[PASSED] All linting checks passed"
