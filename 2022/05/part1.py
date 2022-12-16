#!/usr/bin/python3

import re
import sys

def read_crates(fd, crates, crate_names):
    line = fd.readline()
    while line:
        start_pos = 0
        current_crate = -1
        while True:
            start_pos = line.find('[', start_pos)
            if start_pos == -1:
                break
            value = line[start_pos+1]
            if line[start_pos+2] != ']':
                print("Error parsing crates at line: " + line)
                sys.exit(-1)
            # each crate occupies 4 spaces "[x] "
            current_crate = int(start_pos/4)
            start_pos += 4
            next_crate = int(start_pos/4)
            while len(crates) < next_crate:
                crates.append([])
            crates[current_crate].insert(0, value)

        if start_pos == -1 and current_crate == -1:
            # Could not find any '['
            # Find the names of the crate stacks
            line = line.strip()
            # must use extend, if we directly assign line.split() then we replace the current object
            crate_names.extend(line.split())
            # consume empty line
            line = fd.readline().strip()
            if line != "":
                print("Error line after crate definition is not empty")
                sys.exit(-1)
            return
        line = fd.readline()

def read_moves(fd, crates, crate_names):
    # move 1 from 2 to 1

    pattern = re.compile(r"move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)")
    line = fd.readline()
    while line:
        match = re.search(pattern, line)
        if not match:
            print("Failed to process move line: " + line)
            sys.exit(-1)
        (amount, from_name, to_name) = match.group(1, 2, 3)
        amount = int(amount)
        from_pos = crate_names.index(from_name)
        to_pos = crate_names.index(to_name)
        while amount > 0:
            crates[to_pos].append(crates[from_pos].pop())
            amount = amount - 1
        line = fd.readline()

def print_crates(crates, crate_names):
    for (name, stack) in zip(crate_names, crates):
        print(name, stack)

def main(args):
    # list of all the stacks of crates
    crates=[]
    # list with names of all the crates
    crate_names=[]

    input = args[1]
    with open(input, 'rt') as fd:
        read_crates(fd, crates, crate_names)
        #print_crates(crates, crate_names)
        read_moves(fd, crates, crate_names)
        print_crates(crates, crate_names)

    # top of each stack
    print ("".join(map(lambda x: x[-1], crates)))

if __name__ == '__main__':
    main(sys.argv)
