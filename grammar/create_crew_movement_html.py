#!/usr/bin/env python3

from jinja2 import Environment, PackageLoader, select_autoescape

import os
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

def cdlfile_to_html(content : CdlFile, identifier):
    env = Environment(
        loader=PackageLoader('web_content'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('crew_movements_html.template')
    

    dt_format = "%Y-%m-%d&nbsp;%H%M"
    dt_short_format = "%d/%m&nbsp;%H%M"

    context = list(content.vesselSeasons.values())
    return template.render({
        "vessel_seasons": context, 
        "filename": identifier,
        "file_modified_timestamp": datetime.fromtimestamp(os.path.getmtime(identifier)).strftime("%d/%m/%Y, %H:%M:%S")})

    return

if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filename = argv[1]
    try:
        analyser = CdlFileAnalyser()
        fin = preprocess_named_file(filename)
        content = analyser.analyse(fin)
        for vs in content.vesselSeasons.values():
            schedule_season(vs)
        output = cdlfile_to_html(content, filename or "stdin")
        for line in output:
            stdout.write(line)
    except Exception as e:
        raise e
        die(str(e))
