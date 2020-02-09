#!/usr/bin/env python3
#
# Create the cabin allocation table(s) from a CDL file
#


from jinja2 import Environment, PackageLoader, select_autoescape

import os
from sys import argv, stderr, stdout
from cdl_preprocessor import preprocess_named_file
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from datetime import timedelta, datetime
from grammar_model import CdlFile

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

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

    template = env.get_template('cabins_html.template')
    

    dt_format = "%Y-%m-%d&nbsp;%H%M"
    dt_short_format = "%d/%m&nbsp;%H%M"

    context = list(content.vesselSeasons.values())
    return template.render({
        "vessel_seasons": context, 
        "filename": identifier,
        "file_modified_timestamp": datetime.fromtimestamp(os.path.getmtime(identifier)).strftime("%d/%m/%Y, %H:%M:%S")})

    return

def build_cabin_manifest(vs):

    # the cabin manifest lists the occupants of each cabin for each day of the cruise
 
    manifest = []

    for single_date in daterange(vs.get_first_event_date(), vs.get_last_event_date()):
        entry = {}
        entry['date'] = single_date.strftime("%Y-%m-%d")

        for cabin in vs.vessel.cabins.values():
            occupants = cabin.get_occupants(single_date)
            ids = ""
            for crew in occupants:
                ids += crew.identifier + " "
            entry[cabin.identifier] = ids
        manifest.append(entry)
    return manifest

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
            vs.__dict__["cabin_manifest"] = build_cabin_manifest(vs)

        output = cdlfile_to_html(content, filename or "stdin")
        for line in output:
            stdout.write(line)
    except Exception as e:
        raise e
        die(str(e))
