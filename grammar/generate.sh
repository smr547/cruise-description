#!/bin/bash

echo "Usage: source generate.sh"

antlr4 -visitor -Dlanguage=Python3 Cdl.g4
