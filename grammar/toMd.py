#!/usr/bin/env python3

from io import StringIO
from sys import argv, stderr, stdout
from cdl_preprocessor import preprocess_named_file
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from datetime import timedelta
from model import CdlFile

def hours(td : timedelta):
    secs = td.total_seconds()
    hours = round(secs/3600.0)
    return hours

def die(message):
    stderr.write(str(message) + "\n")
    exit(1)

def cdlfile_to_MD(content : CdlFile):
    
    output = StringIO()

    dt_format = "%Y-%m-%d&nbsp;%H%M"
    dt_short_format = "%d/%m&nbsp;%H%M"
    #dt_short_format = "%m-%d&nbsp;%H%M"
    for vs in content.vesselSeasons.values():
        output.write("# %s\n" % (vs.identifier(), ))
        output.write("Generated from file %s\n" % (filename, ))
        schedule_season(vs)
          
        # display some results

        for c in vs.cruises:
            output.write("## %s\n" % (c.name, ))
            output.write(c.get_description())
            output.write("\n")
            output.write("\n")

            output.write("Date/time    | Event | From<br/>To | Comment\n")
            output.write("------------ | ----- | --------- | ------------------\n")
#            visits = c.get_visitations()
#            v = visits[0]
#            print("%s | depart | %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))

            for leg in c.legs:
                visits = leg.visitations
                from_v = visits[0]
                to_v = visits[-1]
                times = "%s<br/>%s" % (
                    from_v.get_departure_dt().strftime(dt_short_format),
                    to_v.get_arrival_dt().strftime(dt_short_format))

                events = "depart<br/>arrive"
                locs = "%s<br/>%s" % (from_v.location.identifier, to_v.location.identifier)
                comments = ""
                comments += "<br/>stay in %s is  %s hours (expected %d)" % (
                    to_v.location.identifier,
                    hours(to_v.get_computed_duration()),
                    hours(to_v.get_planned_duration_td()))
                for w in leg.get_warnings():
                    comments += "<br/>&#x1F534; %s" % (w.get_message())

                output.write("%s | %s | %s | %s\n" % (times, events, locs, comments[5:]))
    output.seek(0)
    return output

#            for i in range(1,len(visits)-1):
#                v = visits[i]
#                if v.is_stopover():
#                    desc = "stay %s hours (expected %d)" % (
#                        hours(v.get_computed_duration()),
#                        hours(v.get_planned_duration_td()))
#                    for w in v.get_warnings():
#                        desc += "</br>%s" % (w.get_message())
#                    print("%s | arrive | %s | %s" % (v.get_arrival_dt().strftime(dt_format), 
#                        v.location.identifier,
#                        desc))
#                    desc = ""
#                    for w in v.get_warnings():
#                        desc += "</br>%s" % (w.get_message())
#                    print("%s | depart | %s | %s" % (
#                        v.get_departure_dt().strftime(dt_format), 
#                        v.location.identifier, 
#                        desc[5:]))
#                else:
#                    print("%s | waypoint | %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))
#            v = visits[-1]
#            print("%s | arrive |  %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))
#            print("")            

if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filename = argv[1]
    try:
        analyser = CdlFileAnalyser()
        fin = preprocess_named_file(filename)
        content = analyser.analyse(fin)
        output = cdlfile_to_MD(content)
        for line in output:
            stdout.write(line)
    except Exception as e:
        die(str(e))
