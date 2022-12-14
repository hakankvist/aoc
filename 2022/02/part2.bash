#!/bin/bash

# set -x

# A ROCK
# B PAPER
# C SCISSORS
# X need to loose
# Y need to end in draw
# Z need to win
# 0 if lost
# 3 if draw
# 6 if won

ord() {
  LC_CTYPE=C printf '%d' "'$1"
}

total=0
while read line; do
    score=0
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')
    # convert to integers, in range 0-2
    opponent=$(($(ord $(echo $trimmed_line|cut -d ' ' -f 1)) - $(ord 'A')))
    outcome=$(echo $trimmed_line|cut -d ' ' -f 2)

    if [ $outcome = "Y" ]; then
        # end in draw
        me=$opponent
    elif [ $outcome = "X" ]; then
        # need to loose, add 3 since negative numbers are not handled ok
        me=$((($opponent+3-1)%3))
    else
        # need to win
        me=$((($opponent+1)%3))
    fi

    score=$(($me + 1))
    if [ $opponent -eq $me ]; then
        # draw
        score=$(($score + 3))
    elif [ $(($opponent+1)) -eq $me ] || ([ $opponent -eq 2 ] && [ $me -eq 0 ]); then
        # won
        score=$(($score + 6))
    fi
    echo $score " me: " $me " : " $line
    total=$(($score + $total))
done < $1
echo "Total: $total"

