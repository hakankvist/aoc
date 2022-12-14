#!/bin/bash

MAX_CALS=0
CURRENT=0
while read line; do
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')
    if [ -n "$trimmed_line" ]
    then
        CURRENT=$(($CURRENT + $trimmed_line))
    else
        if [ $MAX_CALS -lt $CURRENT ]
        then
            MAX_CALS=$CURRENT
        fi
        CURRENT=0
    fi
done < $1

echo $MAX_CALS
