#!/usr/bin/env python3

__author__ = 'smr'

from sys import stdin, stdout, stderr, exit, argv
from io import StringIO

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

def preprocess(cdl_filename=None):
        '''
        Preprocess the supplied filename, or stdin 
        and return a StringIO object containing the preprocessed source
        '''
        # select input stream

        output = StringIO()
        if cdl_filename is None:
            fin = stdin
        else:
            fin = open(cdl_filename, 'r')

        # read source into memory, including files where specified

        for line in fin:
            if line.startswith("$include "):
                filename = line[8:-1].strip()
                with open(filename) as f:
                    for rec in f:
                        output.write(rec)
            else:
                output.write(line)
        fin.close()
        output.seek(0)
        return output

if __name__ == '__main__':
    filename = None
    if len(argv) > 1:
        filename = argv[1]

    output = preprocess(filename)

    for line in output:
        stdout.write(line)
    output.close()
