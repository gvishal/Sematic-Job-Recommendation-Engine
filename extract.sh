#!/bin/bash

i=1
for txt in $(ls -1 data/txts/);do

    echo "------------"
    echo "data/txts/$txt:"
    grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b" "data/txts/$txt"|sort|uniq
    grep -E -o "([(]?\+[0-9]{1,3}[)]?[- ]?)?[0-9]{10}" "data/txts/$txt"|sort|uniq
    sed '/^[^0-9a-zA-Z]*$/d' "data/txts/$txt"|head -n 1|cut -d' ' -f1,2

    i=$((i+1))
done
