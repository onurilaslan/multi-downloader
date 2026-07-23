#!/usr/bin/env bash

# Determine the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the multi-platform downloader script using the project's virtual environment
"$DIR/venv/bin/python3" "$DIR/reel_downloader.py" "$@"
