#!/bin/bash

# A, X ROCK
# B, Y PAPER
# C, Z SCISSORS
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
    me=$(($(ord $(echo $trimmed_line|cut -d ' ' -f 2)) - $(ord 'X')))

    score=$(($me + 1))
    if [ $opponent -eq $me ]; then
        # draw
        score=$(($score + 3))
    elif [ $(($opponent+1)) -eq $me ] || ([ $opponent -eq 2 ] && [ $me -eq 0 ]); then
        # won
        score=$(($score + 6))
    fi
    echo $score " : " $line
    total=$(($score + $total))
done < $1
echo "Total: $total"

