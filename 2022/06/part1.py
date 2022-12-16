#!/usr/bin/python3

import sys

def analyze_line(line):
    pos = 4
    while pos < len(line):
        sub_string = line[pos-4:pos]
#        print (sub_string)
        chars_set = set(sub_string)
#        print (chars_set)
        if len(chars_set) == 4:
            # if set has four items, then we have found four individual characters
            break
        pos = pos + 1
    print(pos)

def main(args):
    with open(args[1], 'rt') as fd:
        for line in fd:
            analyze_line(line)

if __name__ == '__main__':
    main(sys.argv)
