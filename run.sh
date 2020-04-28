#!/bin/sh

PYTHONPATH=$PYTHONPATH:$(pwd) && echo $PYTHONPATH && export PYTHONPATH

python3 eshop/app.py
