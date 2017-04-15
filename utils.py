def numbers_of_len(n):
    return 9 * (10 ** (n-1))


def distanse_to_int(i):
    length = len(str(i))
    distanse = sum(n * numbers_of_len(n) for n in range(1, length))
    distanse += length * (i - 10 ** (length-1))
    return distanse
