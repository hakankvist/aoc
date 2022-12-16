#!/bin/bash

#set -x

function check () {
    local elf1=$1
    local elf2=$2

    local elf1_low=$(echo -n $elf1|cut -d- -f1)
    local elf1_high=$(echo -n $elf1|cut -d- -f2)

    local elf2_low=$(echo -n $elf2|cut -d- -f1)
    local elf2_high=$(echo -n $elf2|cut -d- -f2)

    if ([ $elf1_low -le $elf2_low ] && [ $elf1_high -ge $elf2_high ]) || \
           ([ $elf1_low -ge $elf2_low ] && [ $elf1_high -le $elf2_high ])
    then
        echo 1
    else
        echo 0
    fi
}


total=0
while read line; do
    trimmed_line=$(echo $line|sed 's/^ *//;s/ *$//')
    elf1=$(echo -n $line|cut -d, -f1)
    elf2=$(echo -n $line|cut -d, -f2)

    contained=$(check $elf1 $elf2)
    if [ $contained -eq 1 ]; then
        total=$(($total+1))
    fi
done < $1
echo "Total: $total"

