#!/usr/bin/env python3

__author__ = 'smr'

from urllib.parse import urlparse
from urllib.request import urlopen
from sys import stdin, stdout, stderr, exit, argv
from io import StringIO

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

def preprocess_named_file(cdl_filename=None):
    '''
    Preprocess the supplied filename, or stdin 
    and return a StringIO object containing the preprocessed source
    '''
    if cdl_filename is None:
        fin = stdin
    else:
        fin = open(cdl_filename, 'r')
    return preprocess(fin)
    

def preprocess(fin):
    '''
    Preprocess the supplied file like object
    and return a StringIO object containing the preprocessed source
    '''
    # select input stream

    output = StringIO()

    # read source into memory, including files where specified
    line_no = 1
    for line in fin:
        if line.startswith("use "):
            url = line[4:-1].strip()
            # check that's its a valid URL
            p = urlparse(url)
            if len(p.scheme) == 0:
                raise Exception("Cannot understand the URL in the 'use' statement at line %s (%s)" % (
                    line_no,
                    url ))
            try:
                with urlopen(url) as f:
                    for rec in f:
                        rec = rec.decode('utf-8')
                        if rec.startswith("#"):
                            pass    # its a comment line
                        else:
                            output.write(rec)
            except Exception as e:
                raise Exception("Cannot use URL at line %s (%s)\n%s" % (
                    line_no,
                    url,
                    str(e)))

        # leave comment lines out
        elif line.startswith("#"):
            pass    # its a comment line
        else:
            output.write(line)
        line_no += 1

    fin.close()
    output.seek(0)
    return output

if __name__ == '__main__':
    try:
        filename = None
        if len(argv) > 1:
            filename = argv[1]

        output = preprocess_named_file(filename)

        for line in output:
            stdout.write(line)
        output.close()
    except Exception as e:
         die(str(e))
