#!/usr/bin/env python3

import argparse
import io
import re
import sys

def skip_first_header(input: io.TextIOBase, output: io.TextIOBase):
    for line in input:
        output.write(line)
        if line.find('/h1') != -1:
            break

def demote_headers(input: io.TextIOBase, output: io.TextIOBase):
    headertag = re.compile(r'(?<=<|/)h(\d)')
    for line in input:
        pos = 0
        while (match := headertag.search(line, pos)) is not None:
            level = int(match[1])
            output.write(line[pos:match.start(1)])
            output.write(str(level + 1))
            pos = match.end(1)
        output.write(line[pos:])

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='Adds one level to all html header tags following the first h1')
    parser.add_argument('-o', dest='outfile', type=argparse.FileType('w'), default=sys.stdout, help='Write output to a file instead of stdout')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Read output from a file instead of stdin')
    options = parser.parse_args(argv[1:])

    input: io.TextIOBase = options.infile
    output: io.TextIOBase = options.outfile
    skip_first_header(input, output)
    demote_headers(input, output)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
