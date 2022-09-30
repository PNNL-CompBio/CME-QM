#!/bin/bash
export PYTHON_BIN=/home/scicons/cascade/apps/python/3.7/bin
export PYTHONHOME=/home/scicons/cascade/apps/python/3.7
export PYTHONPATH=/home/scicons/cascade/apps/python/3.7/lib/python3.7:/home/scicons/cascade/apps/python/3.7/include/python3.7m:/home/scicons/cascade/apps/python/3.7/pkgs
export PATH=${PYTHON_BIN}:${PATH}

echo -e $PYTHON_BIN "\n" $PYTHONHOME "\n" $PYTHONPATH "\n" $PATH