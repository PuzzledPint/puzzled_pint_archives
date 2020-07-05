#!/bin/bash

HERE=`pwd`

python3 -m virtualenv -p python3 ${HERE}/venv
source ${HERE}/venv/bin/activate
pip3 install -r ${HERE}/requirements.txt
python3 ./generator/generator.py archives static

