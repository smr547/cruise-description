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

            print("Date/time    | Event | Destination | Comment")
            print("------------ | ----- | ----------- | ------------------")
            visits = c.get_visitations()
            v = visits[0]
            print("%s | depart | %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))

            for i in range(1,len(visits)-1):
                v = visits[i]
                if v.is_stopover():
                    print("%s | arrive | %s | stay %d hours (expected %d)" % (v.get_arrival_dt().strftime(dt_format), 
                        v.location.identifier,
                        hours(v.get_computed_duration()),
                        hours(v.get_planned_duration_td())))
                    print("%s | depart | %s | " % (v.get_departure_dt().strftime(dt_format), 
                        v.location.identifier))
                else:
                    print("%s | waypoint | %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))
            v = visits[-1]
            print("%s | arrive |  %s |" % (v.get_arrival_dt().strftime(dt_format), v.location.identifier))
            print("")            

        

