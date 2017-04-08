#!/usr/bin/env python3.6

import sys


def get_answer(sequence):
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sequence = input('Enter the sequence: ')
    else:
        sequence = sys.argv[1]

    if not sequence.isdecimal():
        print(f'"{sequence}" is not decimal!', file=sys.stderr)
        sys.exit(1)

    print(sequence)
