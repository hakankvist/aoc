#!/bin/bash

ord() {
  LC_CTYPE=C printf '%d' "'$1"
}

total=0
while read line; do
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')
    com_length=$(($(echo $line|wc -c)/2))
    com1=$(echo -n $line|head -c $com_length)
    com2=$(echo -n $line|tail -c $com_length)

    item=$(comm -1 -2 <( echo $com1|sed 's/./\0\n/g'|sort ) <( echo $com2|sed 's/./\0\n/g'|sort ) | grep -v -e '^$' | tr ' ' '\n'|sort -n |uniq)

    item_value=$(ord $item)
    if [ $item_value -ge $(ord 'a') ] && [ $item_value -le $(ord 'z') ]; then
        item_value=$(($item_value - $(ord 'a') + 1))
    elif [ $item_value -ge $(ord 'A') ]  && [ $item_value -le $(ord 'Z') ]; then
        item_value=$(($item_value - $(ord 'A') + 27))
    else
        echo "Error: "
        exit 1
    fi

    total=$(($total + $item_value))

done < $1
echo "Total: $total"

