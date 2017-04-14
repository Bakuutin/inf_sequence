import pytest
from inf_sequence import get_answer


test_sequences = [
    '21324',
    '24324',
    '0244',
    '01',
] + [str(i) for i in range(50)]

long_test_string = ''.join(map(str, range(1, 100000)))

@pytest.mark.parametrize("sequence", test_sequences)
def test_sequence_finder(sequence):
    print(sequence, long_test_string.find(sequence) - get_answer(sequence))
    # assert long_test_string.find(sequence) == get_answer(sequence)
