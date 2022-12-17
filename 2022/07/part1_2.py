#!/usr/bin/python3

import re
import sys

class dir_node():
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.dirs = {}
        self.files = {}
        self.total_size = -1

    def calculate_sizes(self):
        self.total_size = sum(self.files.values())
        for d in self.dirs.values():
            d.calculate_sizes()
            self.total_size = self.total_size + d.total_size
        return self.total_size

    def __str__(self):
        return "name: %s %s %s" % (self.name, self.dirs, self.files)

def cd(node, name):
    if name == ROOT_NODE.name:
        return ROOT_NODE
    if name == "..":
        return node.parent

    if name not in node.dirs:
        node.dirs[name] = dir_node(node, name)

    return node.dirs[name]

def ls_line(node, dir_list):
    (type_size, name) = dir_list
    if type_size == 'dir':
        node.dirs[name] = dir_node(node, name)
    else:
        node.files[name] = int(type_size)

CD_COMMAND = re.compile(r"\$\s*cd\s*(.*)$")
LS_COMMAND = re.compile(r"\$\s*ls\s*$")
def read_command(fd, node):
    line = fd.readline()
    line = line.strip()
    ls_command_active = False
    while line:
        cd_match = re.match(CD_COMMAND, line)
        ls_match = re.match(LS_COMMAND, line)
        if cd_match:
            ls_command_active = False
            node = cd(node, cd_match.group(1))
        elif ls_match:
            ls_command_active = True
        elif ls_command_active:
            data = line.split(" ", 1)
            ls_line(node, data)
        else:
            print("Error, could not parse command")
            print(line)
            sys.exit(-1)
        line = fd.readline()
        line = line.strip()

ROOT_NODE = dir_node(None, "/")
ROOT_NODE.parent = ROOT_NODE

def find_at_most_sum(node, limit):
    size = node.total_size if node.total_size <= limit else 0
    return size + sum(map(lambda x: find_at_most_sum(x, limit), node.dirs.values()))

def find_delete_dir(node, limit):
    if node.total_size < limit:
        return ROOT_NODE.total_size
    best_limit = ROOT_NODE.total_size
    for d in node.dirs.values():
        size = find_delete_dir(d, limit)
        if size >= limit and size < best_limit:
            best_limit = size

    if node.total_size < best_limit:
        best_limit = node.total_size
    return best_limit

def main(args):
    with open(args[1], 'rt') as fd:
        node = ROOT_NODE
        read_command(fd, node)
    ROOT_NODE.calculate_sizes()
    print("Total size: %d for wanted subtrees" % find_at_most_sum(ROOT_NODE, 100000))
    print("Total size occupied: %d" % ROOT_NODE.total_size)
    needed_size = 30000000 - (70000000 - ROOT_NODE.total_size)
    print("Need to free up minimum: %d" % needed_size)
    print("Total size: %d for directory to be deleted" % find_delete_dir(ROOT_NODE, needed_size))

if __name__ == '__main__':
    main(sys.argv)
