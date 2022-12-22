#!/usr/bin/python3

import re
import sys

def set_hidden(plot, pos):
    # do not change value if already set, because then it is already set as hidden or visible
    if pos not in plot:
        plot[pos] = 0

def set_visible(plot, pos):
    # if it can be seen from one direction, then it can be seen
    if pos == (2,2):
        raise Exception
    plot[pos] = 1

def seen_trees(lines, x, y):
    sum = 1
    height = int(lines[y][x])

    seen = 0
    dx = x - 1
    while dx >= 0:
        seen = seen + 1
        if int(lines[y][dx]) >= height:
            break
        dx = dx -1
    if seen > 0:
        sum = sum * seen

    seen = 0
    dx = x + 1
    while dx < len(lines[y]) :
        seen = seen + 1
        if int(lines[y][dx]) >= height:
            break
        dx = dx + 1
    if seen > 0:
        sum = sum * seen


    seen = 0
    dy = y - 1
    while dy >= 0:
        seen = seen + 1
        if int(lines[dy][x]) >= height:
            break
        dy = dy - 1
    if seen > 0:
        sum = sum * seen

    seen = 0
    dy = y + 1
    while dy < len(lines):
        seen = seen + 1
        if int(lines[dy][x]) >= height:
            break
        dy = dy + 1
    if seen > 0:
        sum = sum * seen

    return sum

def main(args):
    lines = []
    with open(args[1], 'rt') as fd:
        line = fd.readline()
        line = line.strip()
        while line:
            lines.append(list(line))
            line = fd.readline()
            line = line.strip()

    visible = {}
    y = 0
    while y < len(lines):
        left_max = 0
        left_pos = 0
        right_pos = len(lines[0])-1
        right_max = right_pos
        while left_pos < len(lines[0]):
            if lines[y][left_pos] > lines[y][left_max] or left_pos == 0:
                left_max = left_pos
                set_visible(visible, (left_pos,y))
            else:
                set_hidden(visible, (left_pos,y))
            left_pos = left_pos + 1
        while right_pos > 0:
            if lines[y][right_pos] > lines[y][right_max] or right_pos == len(lines[0])-1:
                right_max = right_pos
                set_visible(visible, (right_pos,y))
            else:
                set_hidden(visible, (right_pos,y))
            right_pos = right_pos - 1
        y = y +1

    # Assume all lines are the same length
    x = 0
    while x < len(lines[0]):
        bottom_max = 0
        bottom_pos = 0
        top_pos = len(lines)-1
        top_max = top_pos
        while bottom_pos < len(lines):
            if lines[bottom_pos][x] > lines[bottom_max][x] or bottom_pos == 0:
                bottom_max = bottom_pos
                set_visible(visible, (x,bottom_pos))
            else:
                set_hidden(visible, (x,bottom_pos))
            bottom_pos = bottom_pos + 1
        while top_pos > 0:
            if lines[top_pos][x] > lines[top_max][x] or top_pos == len(lines)-1:
                top_max = top_pos
                set_visible(visible, (x,top_pos))
            else:
                set_hidden(visible, (x,top_pos))
            top_pos = top_pos - 1
        x = x + 1

    x = 0
    y = 0
    max_seen = 0
    while x < len(lines[0]):
        y = 0
        while y < len(lines):
            seen = seen_trees(lines, x, y)
            if seen > max_seen:
                max_seen = seen
                print("Maximum position at: %d, %d: seen %d value :%s" % (x, y, seen, lines[y][x]))
            y = y + 1
        x = x +1

    visible = [(k,v) for (k,v) in visible.items() if v==1]
#    print(visible)
    print("Assignement 1 %d" % len(visible))
    print("Max visible: %d" % max_seen)

if __name__ == '__main__':
    main(sys.argv)
