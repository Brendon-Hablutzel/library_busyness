#!/bin/bash

PYTHON_CMD="python3"

if [ "${1}" = ""  ]; then
	echo "ERROR: an option (export or import) is required as the first argument"
	exit 1
fi

if [ "${1}" = "import"  ]; then
	echo "Importing from data/import/..."
	$PYTHON_CMD import.py
	exit 0
fi

if [ "${1}" = "export"  ]; then
	echo "Exporting to data/export/..."
	$PYTHON_CMD export.py
	exit 0
fi

echo "ERROR: invalid option, expected 'export' or 'import'"
exit 1
