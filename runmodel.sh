#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <key>"
    exit 1
fi

# key=$(cat "$1")
key=$1

ssh -i $key -p 22001 student-admin@paffenroth-23.dyn.wpi.edu "cd CS553-Case-Study-1 && source venv/bin/activate && python3 app.py"
