#!/bin/bash
#   script: time-docker-build.sh
#
#   All command line arguments are passed to docker build command.
#
#   usage: sh time-docker-build.sh  --no-cache=true \
#                         --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
#                         --build-arg BUILD_VERSION=0.0.0 \
#                         -t gitlab.pnnl.gov:4567/anub229/darpacme:0.0.0 -f Dockerfile > inspect/darpacme000.json
#

DATE_FORMAT="+%s"

(
  # Output START line
  echo "$(date $DATE_FORMAT) | - 0 - START"

  docker build $* . |
    grep "^Step" |
    while read line; do
      # Output build output prefixed with date
      echo "$(date $DATE_FORMAT) | $line"
    done

  # Output END line
  echo "$(date $DATE_FORMAT) | - -1 - END"
) | (
  # Generate JSON array output.
  #   - START is step: 0
  #   - END is step: -1

  echo "["
  FIRST_RUN=true
  while read line; do
    [[ -z "$FIRST_RUN" ]] && echo "," # if not first line, print ','

    lineArray=($line)
    time="${lineArray[0]}"  # step is 0th
    step="${lineArray[3]}"  # step is 2nd
    cmd="${lineArray[@]:5}" # cmd is everything after 5th

    stepNum=${step/\/*/}
    escapedCmd="${cmd//\"/\\\"}" # escape all double quotes '"'

    echo "  {"
    echo "    \"time\": $time,"
    echo "    \"step\": $stepNum,"
    echo "    \"cmd\": \"$escapedCmd\""
    echo -n "  }"

    unset FIRST_RUN
  done
  echo
  echo "]"
)
