"""
Находит первое вхождение введённой последовательности в последовательность,
полученную склейкой всех натуральных чисел
"""
from string import *

first100 = ''
for i in range(1, 1000):
    first100 += str(i)
print(first100)


def num_of_crosses(str):
    """
    Возвращает количество 'x' в начале или конце строки
    """
    num = 0
    for char in str:
        if char == 'x':
            num += 1
        else:
            break
    for char in str[::-1]:
        if char == 'x':
            num += 1
        else:
            break
    return num


def num_of_zero(str):
    """
    Возвращает количество нулей в начале строки
    """
    num = 0
    for char in str:
        if char == '0':
            num += 1
        else:
            break
    return num


def fill_crosses(segment, num):
    crosses = num_of_crosses(segment)
    full_num = num.zfill(crosses)
    split_chars = [char for char in segment]
    split_num = [char for char in full_num]
    if segment[0] is 'x':
        for i in range(0, crosses):
            split_chars[i] = split_num[i]
    else:
        split_chars.reverse()
        split_num.reverse()
        for i in range(0, crosses):
            split_chars[i] = split_num[i]
        split_chars.reverse()
    new_segment = ''
    for element in split_chars:
        new_segment += element
    return new_segment


def min_num_to_fill(num_of_crosses, side):
    if num_of_crosses is 0 or side is 'r':
        return 0
    else:
        return int('1'+'0'*(num_of_crosses-1))


def max_num_to_fill(num_of_crosses):
    if num_of_crosses is 0:
        return 0
    return int('9'*num_of_crosses)



def is_empty(segment):
    """
    Проверяет, есть ли в сегменте цифры
    """
    for char in segment:
        if char != 'x':
            return False
    return True


def to_segment(str_seq, segment_len, shift):
    """
    Делит строку на list из значащих сегментов
    """
    ext_str_seq = segment_len*'x'+str_seq+segment_len*'x'
    segments = [ext_str_seq[num+shift:num+segment_len+shift]
                for num in range(0, len(ext_str_seq), segment_len)
                if not is_empty(ext_str_seq[num+shift:num+segment_len+shift])
                ]
    return segments

"""
def find_distance(num):
    summ = -1
    num_len = len(str(num))
    digit_list = [int(digit) for digit in str(num)]
    digit_list.reverse()
    for i in range(0, num_len):
        step = digit_list[i] * (num_len-i)
        for j in range(0, num_len-i):
            step *= 10
        summ += step
    print(summ)
"""


def are_equivalent(num, segment):
    if num == segment:
        return True
    digit_list = [char for char in segment]
    if len(digit_list) is 0:
        return True
    num_list = [char for char in num]
    if len(num_list) < len(digit_list):
        return False
    if segment[-1] is 'x':
        for i in range(0, len(digit_list)-1):
            if num_list[i] != digit_list[i] and digit_list[i] != 'x':
                return False
    else:
        num_list.reverse()
        digit_list.reverse()
        for i in range(0, len(digit_list)):
            if num_list[i] != digit_list[i] and digit_list[i] != 'x':
                return False
    return True


def min_num_in_segments(segments):
    if segments[0][0] is '0':
        return [float('Inf'), 0]
    if len(segments) is 1:
        if segments[0][0] is 'x':
            return [
                fill_crosses(segments[0],
                                str(min_num_to_fill(num_of_crosses(segments[0]), 'l'))),
                num_of_crosses(segments[0])]
        elif segments[0][-1] is 'x':
            return [
                fill_crosses(segments[0],
                                str(min_num_to_fill(num_of_crosses(segments[0]), 'r'))),
                num_of_crosses(segments[0])]
        return [segments[0],
                num_of_crosses(segments[0])]

    full_segments = [segment for segment in segments
                     if not 'x' in segment and len(segment) != 0]
    for segment in full_segments:
        if segment[0] is '0':
            return [float('Inf'), 0]
    if len(full_segments) > 1:
        for i in range(0, len(full_segments)-1):
            if int(full_segments[i])+1 != int(full_segments[i+1]):
                return [float('Inf'), 0]
    if len(full_segments) == len(segments):
        return [segments[0],
                num_of_crosses(segments[0])]

    if segments[0][0] is 'x':
        for i in range(min_num_to_fill(num_of_crosses(segments[0]), 'l'),
                       max_num_to_fill(num_of_crosses(segments[0]))):
            filled = fill_crosses(segments[0], str(i))
            correct = True
            for j in range(1, len(segments)):
                test = (str(int(filled)+j), segments[j])
                if not are_equivalent(str(int(filled)+j), segments[j]):
                    correct = False
            if correct is True:
                return [filled,
                        num_of_crosses(segments[0])]
    if segments[-1][-1] is 'x':
        for i in range(min_num_to_fill(num_of_crosses(segments[-1]), 'r'),
                       max_num_to_fill(num_of_crosses(segments[-1]))):
            filled = fill_crosses(segments[-1], str(i))
            correct = True
            for j in range(1, len(segments)):
                if not are_equivalent(str(int(filled)-j), segments[-j+1]):
                    correct = False
            if correct is True:
                return [filled,
                        num_of_crosses(segments[0])]
    return [float('Inf'), 0]


def split_seq(str_seq):
    nums = dict()
    for segment_len in range(1, len(str_seq)+1+num_of_zero(str_seq)):
        for shift in range(0, segment_len):
            segments = to_segment(str_seq, segment_len, shift)
            min_num = min_num_in_segments(segments)
            if min_num[0] != float('Inf'):
                nums[int(min_num[0])] = min_num[0]
            print(segments)
            print(min_num_in_segments(segments))
    return nums[min(nums.keys())]
#print(split_seq('627'))
find_distance(10)
#str_seq = input('Введите искомую последовательность: ')
print(first100.find('10'))