#!/usr/bin/env python3

# List all the locations mentioned in a cruise description
#

__author__ = 'smr'

#!/usr/bin/env python3

from sys import argv
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from datetime import datetime, timedelta
import simplekml
from math import ceil

# def hours(td : timedelta):
#     secs = td.total_seconds()
#     hours = round(secs/3600.0)
#     return hours

if __name__ == '__main__':
    filename = argv[1]
    analyser = CdlFileAnalyser()
    content = analyser.analyse(filename)

    dt_format = "%Y-%m-%d %H%M"

    # document

    kml = simplekml.Kml(open=1)
    desc = "Generated from CDL file %s at %s" % (filename, datetime.now().isoformat())
    doc = kml.newdocument(name=filename, description=desc, open=1)

    # locations

    desc = "All of the locations mentioned in the CDL source file"
    loc_folder = doc.newfolder(name="Locations", description=desc, open=0, visibility=0)

    for loc in content.locations.values():
        pnt = loc_folder.newpoint(name=loc.identifier, description=loc.name, coords=[loc.coords])

    # vessel/seasons
    for vs in content.vesselSeasons.values():
        # schedule this season
        schedule_season(vs)
   
        # prepare a folder for each vessel/season

        description = "Plan for vessel %s, %s season" % (vs.vessel.identifier, vs.season)
        vs_folder = doc.newfolder(name=vs.key(), description=desc, open=1)

        # cruises
        for c in vs.cruises:
            desc = "%s cruise, %d nautical miles in %d days" % (c.name, 
                round(c.distance_NM()), 
                int(ceil(c.elapsed_time_td().total_seconds()/86400.0)))
            c_folder = vs_folder.newfolder(name=c.name, description=desc, open=0, visibility=1)

#            # draw the route
#            route = []
#            for v in c.get_visitations():
#                route.append(v.location.coords)
#
#            ls = c_folder.newlinestring(name=c.name)
#            ls.coords = route
#            ls.style.linestyle.width = 10
#            ls.style.linestyle.color = simplekml.Color.red

            # draw it as legs
            leg_no = 0
            for leg in c.legs:
                leg_no += 1
                desc = "%d nautical miles in %d hours." % (
                    round(leg.distance_NM()), 
                    round(leg.sailing_time().total_seconds()/3600.0)) 
                leg_folder = c_folder.newfolder(name=leg.name(), description=desc)

                # draw the route
                route = []
                for v in leg.visitations:
                    route.append(v.location.coords)

                ls = leg_folder.newlinestring(name=leg.name())
                ls.coords = route
                ls.style.linestyle.width = 10
                ls.style.linestyle.color = simplekml.Color.red


    # all done, output the kml

    print(kml.kml())

