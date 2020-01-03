#!/usr/bin/env python3

# Extract the vessel identifier from the supplied cdl file and print to stdout

import traceback
from sys import argv, stderr, stdout
from cdl_preprocessor import preprocess_named_file
from CdlFileAnalyser import CdlFileAnalyser
from grammar_model import CdlFile

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filename = argv[1]
    try:
        analyser = CdlFileAnalyser()
        fin = preprocess_named_file(filename)
        content = analyser.analyse(fin)
        vs = list(content.vesselSeasons.values())[0]
        print(vs.vessel.identifier)
    except Exception as e:
        traceback.print_exc(file=stdout)
        die(str(e))
