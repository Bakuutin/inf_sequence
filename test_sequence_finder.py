import pytest
from inf_sequence import get_answer


test_sequences = [
    '24324',
    '01',
    ''.join(map(str, range(7, 103))),  # 7891011...9899100101102
] + [
    str(i) for i in range(1500)
]

long_test_string = ''.join(map(str, range(1, 1000)))

@pytest.mark.parametrize("sequence", test_sequences)
def test_sequence_finder(sequence):
    assert get_answer(sequence) == long_test_string.find(sequence)
