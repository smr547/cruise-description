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
cp ${tmppath}/schedule.md .
./summary_HTML.py /tmp/${season_id}.cdl > ${tmppath}/summary.html 
./md_html.py ${tmppath}/schedule.md > ${tmppath}/schedule.html
./make_source_html.py ${cdl_file} > ${tmppath}/source.html
cp ${cdl_file} ${tmppath}
rm /tmp/${season_id}.cdl 
content_path=/home/planacruise/web_content/
scp -r /tmp/${vessel_id}  smr@planacruise.online:${content_path}
rm -r ${tmppath}
