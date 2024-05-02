
#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR

FILE=./scripts/export_mapping_diff
if [ -f "$FILE" ]; then
    #echo "$FILE exists."
    cat $FILE
else
    echo "$FILE not exists."
fi

