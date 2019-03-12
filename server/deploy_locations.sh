#!/bin/bash

cd ~/projects/locations
git pull
cd docs
cp *.txt ~/planacruise/content/locations
cp *.cdl ~/planacruise/content/locations
cd ../grammar
./create_locations_kml.sh
