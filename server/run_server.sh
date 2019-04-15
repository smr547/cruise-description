#!/bin/bash
export FLASK_ENV=development
export FLASK_APP=server.py 
export PYTHONPATH=.:../grammar
python3 ~/.local/bin/flask run --host=0.0.0.0 
