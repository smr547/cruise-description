#!/usr/bin/env python3

# Create a summary of the supplied CDL file in HTML format

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

def cdlfile_to_HTML(content : CdlFile, identifier):
    
    output = StringIO()
    output.write("<html>\n")
    output.write("<head>\n")
    output.write("<title>Season Summary</title>\n")
    output.write("</head>\n")

    # framework code for OpenLayers mapping integration

    output.write("<style>#map {\n")
    output.write("width: 900px;\n")
    output.write("height: 500px;\n")
    output.write("}</style>\n")
    output.write('<link rel="stylesheet" href="/cruise_maps/openlayers.e31bb0bc.css">\n')




    output.write("<body>\n")
    output.write("<p>\n")

#   Source file and version timestamp

    path = Path(identifier)
    content_id = path.name
    file_last_modified = datetime.fromtimestamp(os.path.getmtime(identifier))

    output.write("This cruise summary was generated from the file ")
    output.write('<a href="source.html">%s</a> ' % (content_id))
    # output.write('<a href="%s">%s</a> ' % (content_id, content_id))
    output.write(' last modified at %s ' % file_last_modified.strftime("%d/%m/%Y, %H:%M:%S"))
    output.write("</p>\n")

    for vs in content.vesselSeasons.values():

        output.write("<h1>Summary for season %s on vessel %s</h1> \n" % (vs.season, vs.vessel.name))

        output.write("<h2>Season summary</h2> \n")
        output.write("<p>The following table lists the series of cruises planned for the season<br/></p>\n")


        output.write('<table>\n')
        output.write('<tr>\n')
        output.write('<td>\n')
        output.write('<table border="1">\n')
        output.write("<tr><th>Cruise</th><th>Cruise name</th><th>Departure</th><th>Destination</th><th>Duration</th></tr>\n")


        schedule_season(vs)
          
        # display some results
        
        cruise_no = 0
        for c in vs.cruises:
            cruise_no += 1

            departure_text = "%s<br>%s" % (c.departure_port.identifier, c.get_departure_dt().strftime("%d/%m/%Y"))
            destination_text = "%s<br>%s (stay for %s days)" % (c.get_destination_port().identifier, c.get_arrival_dt().strftime("%d/%m/%Y"), c.get_destination_stay_dt().days)
            if c.elapsed_time_td().days == 0:
                duration = "%s hours" % (round(c.elapsed_time_td().seconds/3600.0))
            else:
                duration = "%s days" % (c.elapsed_time_td().days)

            output.write("<tr>")
            output.write("<td>%s</td>" % (cruise_no))
            output.write("<td>%s</td>" % (c.name))
            output.write("<td>%s</td>" % (departure_text))
            output.write("<td>%s</td>" % (destination_text))
            output.write("<td>%s</td>" % (duration))
            output.write("</tr>\n")
            
        output.write("</table>\n")
        output.write('</td>\n')
        output.write('<td>\n')

        # Open layers chart goes here

        output.write('<div id="map"></div>\n')
        output.write('<script src="/cruise_maps/openlayers.e31bb0bc.js"></script>\n') 

        output.write('</td>\n')
        output.write('</tr>\n')
        output.write('</table>\n')



        output.write("<h2>Warning</h2> \n")
        output.write("<p>Please note that yacht cruising is subject to weather, crew health and other saftey concerns.\n")
        output.write("The published schedule is subject to change without notice. Please include flexibility in your flight and accommodation bookings</p>\n")
        output.write("<h2>Further information</h2> \n")
        output.write("<p>For further information regarding this season plan please refere to:\n")
        output.write("</p>\n")
        output.write("<ul>\n")
        output.write('<li><a href="./schedule.html">Detailed season schedule</a></li>\n')
        output.write('<li><a href="./chart.kml">Chart</a> (via Google Earth) -- once the chart.kml file has downloaded, double-click on it to launch Google Earth. ')
        output.write('You may need to load <a href="https://support.google.com/earth/answer/21955?hl=en">install Google Earth</a> on your computer</li>\n')
        output.write("</ul>\n")

        output.write("<h2>Goolge Earth link</h2>\n")
        output.write("<p>To view the chart in Google Earth, use menus options <bold>Add ... Network Link</bold> and paste in the following URL.\n")
        output.write('<textarea rows="1" cols="60" readonly>')
        output.write("http://planacruise.online/%s/%s/chart.kml\n" % (vs.vessel.identifier, vs.season))
        output.write("</textarea>")


    output.write("</body>\n")
    output.write("</html>\n")
    output.seek(0)
    return output

if __name__ == '__main__':

    filename = None
    if len(argv) > 1:
        filename = argv[1]
    try:
        analyser = CdlFileAnalyser()
        fin = preprocess_named_file(filename)
        content = analyser.analyse(fin)
        output = cdlfile_to_HTML(content, filename or "stdin")
        for line in output:
            stdout.write(line)
    except Exception as e:
        raise e
        die(str(e))
