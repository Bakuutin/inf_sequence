import pytest
from inf_sequence import get_best_split
from utils import distanse_to_int


test_sequences = [
    '24324',
    '01',
    ''.join(map(str, range(7, 103))),  # 7891011...9899100101102
] + [
    str(i) for i in range(1500)
]

long_test_string = ''.join(map(str, range(1, 1500)))


@pytest.mark.parametrize("sequence", test_sequences)
def test_sequence_finder(sequence):
    assert get_best_split(sequence).distanse == long_test_string.find(sequence)


@pytest.mark.parametrize("number", range(1, 150))
def test_distanse_finder(number):
    huge_string = ''.join(map(str, range(1, number)))
    assert distanse_to_int(number) == len(huge_string)
