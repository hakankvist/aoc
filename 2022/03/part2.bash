#!/bin/bash

#set -x

ord() {
  LC_CTYPE=C printf '%d' "'$1"
}

total=0

function get_unique_chars ()
{
    local line=$1
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')

    echo $trimmed_line|sed 's/./\0\n/g'|sort|uniq
}

while read -r line1;  do
    read -r line2
    read -r line3

    echo $line1
    echo $line2
    echo $line3
    item=$(echo $(get_unique_chars $line1)$(get_unique_chars $line2)$(get_unique_chars $line3) |tr ' ' '\n' |grep -v -e '^$'|sort|uniq -c |grep 3|awk '{print $NF}')

    echo $item

    item_value=$(ord $item)
    if [ $item_value -ge $(ord 'a') ] && [ $item_value -le $(ord 'z') ]; then
        item_value=$(($item_value - $(ord 'a') + 1))
    elif [ $item_value -ge $(ord 'A') ]  && [ $item_value -le $(ord 'Z') ]; then
        item_value=$(($item_value - $(ord 'A') + 27))
    else
        echo "ERROR " $item_value
        exit 1
    fi

    total=$(($total + $item_value))

done < $1
echo "Total: $total"

