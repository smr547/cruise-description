#!/usr/bin/env python3

import os
from pathlib import Path 
from io import StringIO
from sys import argv, stderr, stdout
from cdl_preprocessor import preprocess_named_file
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from datetime import timedelta, datetime
from grammar_model import CdlFile

def hours(td : timedelta):
    secs = td.total_seconds()
    hours = round(secs/3600.0)
    return hours

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

def create_source_html(filepath):
    
    output = StringIO()
    output.write("<html>\n")
    output.write("<head>\n")
    output.write("<title>CDL source</title>\n")
    output.write("</head>\n")

    output.write("<body>\n")
    output.write("<p>\n")

#   Source file and version timestamp

    path = Path(filepath)
    file_last_modified = datetime.fromtimestamp(os.path.getmtime(filepath))

    output.write("<h1>CDL source file</h1>\n")
    output.write('<p>Content last modified at %s ' % file_last_modified.strftime("%d/%m/%Y, %H:%M:%S"))
    output.write("</p>\n")
    output.write('<textarea rows="60" cols="80" readonly>')
    output.write("\n")

    with open(filepath, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            output.write(line)

    output.write("</textarea>\n")
    output.write("</body>\n")
    output.write("</html>\n")
    output.seek(0)
    return output

if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filepath = argv[1]
    try:
        output = create_source_html(filepath or "stdin")
        for line in output:
            stdout.write(line)
    except Exception as e:
        raise e
        die(str(e))
