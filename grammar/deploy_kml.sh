#!/bin/bash

# Take the specified cdl file as input, generate all web content and deploy to the web server

# exit is any command fails
set -e

cdl_file=$1
season_id=${cdl_file%.cdl}
echo season id is ${season_id}

./cdl_preprocessor.py ${season_id}.cdl > /tmp/${season_id}.cdl 
vessel_id=`./vessel_id.py /tmp/${season_id}.cdl`
echo Vessel is $vessel_id

# create output directory
tmppath=/tmp/${vessel_id}/${season_id}
if [ -d "${tmppath}" ]; then
  rm -r ${tmppath}
fi
mkdir -p ${tmppath} 

# generate files

./toKml.py /tmp/${season_id}.cdl > ${tmppath}/chart.kml 
./toMd.py /tmp/${season_id}.cdl > ${tmppath}/schedule.md 
./summary_HTML.py /tmp/${season_id}.cdl > ${tmppath}/summary.html 
./create_schedule_html.py /tmp/${season_id}.cdl > ${tmppath}/schedule.html 
./create_crew_movement_html.py /tmp/${season_id}.cdl > ${tmppath}/crew_movement.html 
./create_cabins_html.py /tmp/${season_id}.cdl > ${tmppath}/cabins.html 
./make_source_html.py ${cdl_file} > ${tmppath}/source.html
cp ${cdl_file} ${tmppath}
rm /tmp/${season_id}.cdl 
content_path=/home/planacruise/web_content/test/${vessel_id}/
scp -r /tmp/${vessel_id}  smr@planacruise.online:${content_path}
rm -r ${tmppath}
