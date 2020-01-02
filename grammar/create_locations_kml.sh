#!/bin/bash

# Create a ``locations.kml`` file by merging all know location definition ``cdl`` files

src_dir=~/projects/locations/docs
loc_dir=~/planacruise/content/locations
tmpfile=$(mktemp /tmp/cdl-script.XXXXXX)
cp $src_dir/*.txt $loc_dir
echo "vessel Trilogy name: \"Trilogy\" flag: \"Australia\" rego: 12345 speed: 7.5" >> "$tmpfile"
for filename in $loc_dir/*.txt; do
    cat ${filename} >> "$tmpfile"
done
echo "season dummy_season vessel Trilogy begins in Barcelona" >> "$tmpfile"
cat "$tmpfile" | ./cdl_preprocessor.py | ./toKml.py > $loc_dir/locations.kml
rm "$tmpfile"
