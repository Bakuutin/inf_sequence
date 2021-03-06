#!/usr/bin/env python3.6

import sys
import logging
from utils import distanse_to_int


MAX_NUMBER_WIDTH = 10
PAD = '#'
logger = logging.getLogger('sequence')


class InvalidSequence(Exception):
    pass


def split_to_blocks(sequence, width):
    for i in range(0, len(sequence), width):
        yield sequence[i:i + width]


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
        raise InvalidSequence(
            f'{sequence[:len(mask)]}{PAD * (len(mask) - len(sequence))}'
            f' != {expected_next}'
        )


def check_padded_initial_number(shift, mask, sequence):
    expected_next = int(sequence[:shift] + mask) + 1
    if are_mathed(str(expected_next), sequence):
        return expected_next - 1

    elif mask[-1] != '9':
        raise InvalidSequence(
            f'{sequence[:len(mask) + shift]}'
            f'{PAD * (len(mask) + shift - len(sequence))}'
            f' != {expected_next}'
        )

    possible_shift = int(sequence[:shift]) - 1
    possible_current = int(f'{possible_shift}{mask}')
    if are_mathed(str(possible_current + 1), sequence):
        return possible_current
    raise InvalidSequence(
        f'{sequence[:len(mask) + shift]}'
        f'{PAD * (len(mask) + shift - len(sequence))}'
        f' != {possible_current + 1}'
    )


def fill_mask(shift, mask):
    return 10 ** shift + int(mask) if shift else int(mask)


def get_split(width, shift, sequence):
    mask = sequence[:width - shift]
    sequence = sequence[width - shift:]

    if not sequence:
        return Split(fill_mask(shift, mask), shift=shift)

    number = get_initial_number(mask, sequence, shift)

    split = Split(number, shift=shift)

    while sequence:
        str_next = str(number + 1)
        step = len(str_next)  # TODO: ceil&log10
        if not are_mathed(str_next, sequence):
            raise InvalidSequence(
                f'{str_next} != {sequence[:step]}'
                f'{PAD * (step - len(sequence))}'
            )
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

    def __len__(self):
        return distanse_to_int(self.end) - distanse_to_int(self.start)

    @property
    def distanse(self):
        return distanse_to_int(self.start) + self.shift


def get_best_splits(sequence):
    for width in range(1, min(len(sequence) + 2, MAX_NUMBER_WIDTH)):
        splits = []
        for shift in range(width):
            if not shift and sequence.startswith('0'):
                continue
            try:
                splits.append(get_split(width, shift, sequence))
            except InvalidSequence as e:
                invalid_split = list(
                    split_to_blocks(pad(shift, sequence, width), width)
                )
                logger.info(f'Invalid split: {invalid_split} {e}')
        if splits:
            return splits


def get_best_split(sequence):
    splits = get_best_splits(sequence)
    return min(splits, key=lambda s: s.start)


def main():
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        sequence = input('Enter a sequence: ')
    else:
        sequence = sys.argv[1]

    if not sequence.isdecimal():
        print(f'"{sequence}" is not decimal!', file=sys.stderr)
        sys.exit(1)

    from colored import fg, attr
    split = get_best_split(sequence)
    painted = fg("yellow")
    reset = attr('reset')
    string_split = " ".join(map(str, range(split.start, split.end)))
    right_shift = (
        (len(split) - split.shift - len(sequence)) or -len(string_split)
    )
    before = f'{split.start - 1} ' if split.start != 1 else ''
    after = split.end
    colored_string_split = (
        f'{before}'
        f'{string_split[:split.shift]}{painted}'
        f'{string_split[split.shift:-right_shift]}{reset}'
        f'{string_split[-right_shift:]} '
        f'{after}'
    )
    print(colored_string_split)


if __name__ == '__main__':
    main()
