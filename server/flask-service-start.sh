#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# cd $SCRIPTDIR

python $SCRIPTDIR/http_server.py --debug run
# gunicorn -w 1 -b 0.0.0.0:5000 http_server:app --reload
