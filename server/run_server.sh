#!/bin/bash

FLASK_APP=hello.py nohup python3 ~/.local/bin/flask run --host=0.0.0.0 &
