#!/bin/bash
#
# Watch the specified cdl and deploy all generated files upon change
#

cdl_file=$1
fswatch -0 ./${cdl_file} | xargs -0 -n 1 -I {} ./deploy_kml.sh ${cdl_file}
