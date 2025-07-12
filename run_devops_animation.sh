#!/bin/bash

echo "========================================"
echo "   DevOps Animation Launcher"
echo "========================================"
echo ""
echo "Starting DevOps Animation Dashboard..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.6 or higher"
        echo ""
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.6"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python version $PYTHON_VERSION is too old"
    echo "Please install Python 3.6 or higher"
    echo ""
    exit 1
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo ""

# Run the launcher
$PYTHON_CMD run_devops_animation.py

# Check if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred while running the application."
    echo ""
fi 