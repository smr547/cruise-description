#!/bin/bash

cruise=$1
./cdl_preprocessor.py ${cruise}.cdl | ./toKml.py > ${cruise}.kml
./cdl_preprocessor.py ${cruise}.cdl | ./toMd.py > ${cruise}.md &
scp ${cruise}.kml smring@thomas.dreamhost.com:planacruise/content/cruises
