def numbers_of_len(n):
    return 9 * (10 ** (n-1))

def distanse_to_int(i):
    l = len(str(i))
    distanse = sum(n * numbers_of_len(n) for n in range(1, l))
    distanse += l * (i - 10 ** (l-1))
    return distanse
