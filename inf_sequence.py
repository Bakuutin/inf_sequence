#!/usr/bin/env python3.6

import sys
from math import ceil
from collections import namedtuple
from pprint import pprint

PAD = 'x'

class InvalidSequence(Exception):
    pass

Occurence = namedtuple('Occurence', ['first_number', 'shift'])

def split_to_blocks(sequence, width):
    for i in range(0, len(sequence), width):
        yield sequence[i:i+width]

def pad(shift, sequence, width):
    right_pad_len = width - ((shift + len(sequence)) % width)
    if right_pad_len == width:
        right_pad_len = 0
    return f'{PAD * shift}{sequence}{PAD * right_pad_len}'

def get_initial_number(mask, sequence, shift=0):
    assert mask and sequence

    if sequence.startswith('0') or not shift and mask.startswith('0'):
        raise InvalidSequence('Leading zero')

    if shift:
        return check_padded_initial_number(shift, mask, sequence)
    else:
        return check_unpadded_initial_number(mask, sequence)

def are_mathed(a, b):
    common = min(len(a), len(b))
    return a[:common] == b[:common]

def check_unpadded_initial_number(mask, sequence):
    current = int(mask)
    expected_next = current + 1
    if are_mathed(str(expected_next), sequence):
        return current
    else:
        raise InvalidSequence(f'Invalid next {expected_next} != {sequence[:len(mask)]}')

def check_padded_initial_number(shift, mask, sequence):
    expected_next = int(sequence[:shift] + mask) + 1
    if not are_mathed(str(expected_next), sequence):
        raise InvalidSequence(f'Invalid next {expected_next} != {sequence[:len(mask)]}')
    return expected_next - 1

def fill_mask(shift, mask):
    return 10 ** shift + int(mask)


def get_split(width, shift, sequence):
    mask = sequence[:width - shift]
    sequence = sequence[width - shift:]

    if not sequence:
        return Split(fill_mask(shift, mask), shift=shift)

    # import ipdb; ipdb.set_trace()
    number = get_initial_number(mask, sequence, shift)
    split = Split(number, shift=shift)

    while sequence:
        str_number = str(number)
        str_next = str(number + 1)
        step = len(str_number) # TODO: ceil&log10
        if not are_mathed(str_next, sequence):
            raise InvalidSequence(f'Invalid next {str_next} != {sequence[:step]}')
        number += 1
        split.size += 1
        sequence = sequence[step:]

    return split

class Split:
    def __init__(self, start, size=1, shift=0):
        self.size = size
        self.start = start
        self.shift = shift

    def __str__(self):
        return str(list(range(self.start, self.end)))

    def __repr__(self):
        return f'<Split shift="{self.shift}" {self}>'

    @property
    def end(self):
        return self.size + self.start

    @property
    def distanse(self):
        print(repr(self))
        return distanse_to_int(self.start) - self.shift

def numbers_of_len(n):
    return 9 * (10 ** n) - 1

def distanse_to_int(i):
    huge_string = ''.join(map(str, range(1, i)))
    return len(huge_string)


def get_best_splits(sequence):
    for width in range(1, len(sequence) + 2):
        splits = []
        for shift in range(width):
            if not shift and sequence.startswith('0'):
                continue
            try:
                splits.append(get_split(width, shift, sequence))
            except InvalidSequence as e:
                ending = list(split_to_blocks(pad(shift, sequence, width), width))
                # print('not ok:', ending, e)
        if splits:
            return splits

def get_best_split(sequence):
    splits = get_best_splits(sequence)
    return min(splits, key=lambda s: s.start)

def get_answer(sequence):
    return get_best_split(sequence).distanse

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sequence = input('Enter the sequence: ')
    else:
        sequence = sys.argv[1]

    if not sequence.isdecimal():
        print(f'"{sequence}" is not decimal!', file=sys.stderr)
        sys.exit(1)

    pprint(get_answer(sequence))
