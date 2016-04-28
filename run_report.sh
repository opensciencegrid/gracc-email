#!/bin/sh 

# Source the activate file
. $1

shift

# Now, locate and run the report
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$DIR/src/report.py "$@"


