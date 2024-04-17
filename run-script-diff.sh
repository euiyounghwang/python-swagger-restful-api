
#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi

SERVER_INFO_FILE="C://Users//euiyoung.hwang/"

# --
# Shell command
# ./run-script-diff.sh http://localhost:9200 http://localhost:9200

# --
# Test
# python ./scripts/mapping_diff_script.py --test true --es http://localhost:9292/ --ts http://localhost:9292/
# python ./scripts/mapping_diff_script.py --test true --es $1 --ts $2

# Run the command for comparing the mapping between clusters
# python ./scripts/mapping_diff_script.py --es http://localhost:9292/ --ts http://localhost:9292/
python ./scripts/mapping_diff_script.py --es $1 --ts $2 --server_info $SERVER_INFO_FILE



