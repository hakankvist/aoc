#!/bin/bash

CURRENT=0
LIST=""
while read line; do
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')
    if [ -n "$trimmed_line" ]
    then
        CURRENT=$(($CURRENT + $trimmed_line))
    else
        LIST="$LIST $CURRENT"
        CURRENT=0
    fi
done < $1
# Need to add list line as well
LIST="$LIST $CURRENT"

echo $(($(echo $LIST|tr ' ' '\n'|sort -n |tail -3|tr '\n' '+'|sed 's/\+$//')))
