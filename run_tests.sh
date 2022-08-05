#!/bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo "Start virtual environment"
cd $parent_path
source venv/bin/activate

echo "Run tests"
coverage run --source=. --omit="*/__tests__/*" -m unittest discover -v

echo "Run coverage report"
coverage html