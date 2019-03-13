#!/bin/bash

FLASK_APP=server.py nohup python3 ~/.local/bin/flask run --host=0.0.0.0 &
