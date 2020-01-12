#!/usr/bin/env python3

# Create a summary of the supplied CDL file in HTML format

import os
from pathlib import Path 
from io import StringIO
from sys import argv, stderr, stdout
from cdl_preprocessor import preprocess_named_file
from CdlFileAnalyser import CdlFileAnalyser
from datetime import timedelta, datetime 
from grammar_model import CdlFile
from scheduler import schedule_season

def hours(td : timedelta):
    secs = td.total_seconds()
    hours = round(secs/3600.0)
    return hours


if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filename = argv[1]

    analyser = CdlFileAnalyser()
    fin = preprocess_named_file(filename)
    cdl_file = analyser.analyse(fin)

    # schedule all the seasons
  
    for vs in cdl_file.vesselSeasons.values():
         schedule_season(vs)
 
 
    for vs in cdl_file.vesselSeasons.values():
        for c in vs.cruises:
            for e in c.events:
                print(e)

    print("=====================") 
    as_at = datetime.strptime("20/5/2020", "%d/%m/%Y")
    print(type(as_at))
    for vs in cdl_file.vesselSeasons.values():
        vessel = vs.vessel
        cabins = vs.vessel.cabins

        for cabin in cabins.values():
            print("Crew events for ", cabin)

            

            for e in cabin.crew_events:
                print(e)

            occ = cabin.get_occupants(as_at)
            print("occupants at 20/5/2020", occ)

