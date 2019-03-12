#!/usr/bin/env python3

from sys import argv
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from datetime import timedelta

def hours(td : timedelta):
    secs = td.total_seconds()
    hours = round(secs/3600.0)
    return hours

if __name__ == '__main__':
    filename = None
    if len(argv) > 1:
        filename = argv[1]
    analyser = CdlFileAnalyser()
    content = analyser.analyse(filename)

    dt_format = "%Y-%m-%d %H%M"
    for vs in content.vesselSeasons.values():
        print("# %s" % (vs.identifier(), ))
        print("Generated from file %s" % (filename, ))
        schedule_season(vs)
          
        # display some results

        for c in vs.cruises:
            print("## %s" % (c.name, ))
            print(c.get_description())
            print("")

            print("Date/time    | Event | From<br/>To | Comment")
            print("------------ | ----- | --------- | ------------------")
#            visits = c.get_visitations()
#            v = visits[0]
#            print("%s | depart | %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))

            for leg in c.legs:
                visits = leg.visitations
                from_v = visits[0]
                to_v = visits[-1]
                times = "%s<br/>%s" % (
                    from_v.get_departure_dt().strftime(dt_format),
                    to_v.get_arrival_dt().strftime(dt_format))

                events = "departure<br/>arrival"
                locs = "%s<br/>%s" % (from_v.location.identifier, to_v.location.identifier)
                comments = ""
                comments += "<br/>stay in %s is  %s hours (expected %d)" % (
                    to_v.location.identifier,
                    hours(to_v.get_computed_duration()),
                    hours(to_v.get_planned_duration_td()))
                for w in leg.get_warnings():
                    comments += "<br/>&#x1F534; %s" % (w.get_message())

                print("%s | %s | %s | %s" % (times, events, locs, comments[5:]))
                
                
                


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
