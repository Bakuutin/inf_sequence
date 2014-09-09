"""
Находит первое вхождение введённой последовательности в последовательность,
полученную склейкой всех натуральных чисел
"""
from string import *

first100 = ''
for i in range(1, 10005):
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
    return int('9'*num_of_crosses)+1



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


def get_rank_size(rank):
    if rank is 0:
        return 0
    size = '9'
    for i in range(1, rank):
        size += '0'
    return int(size)


def get_min_num(rank):
    min_num = '1'
    for i in range(1, rank):
        min_num += '0'
    return int(min_num)


def find_distance(num):
    summ = 0
    num_len = len(str(num))
    for rank in range(1, num_len):
        summ += rank * get_rank_size(rank)
    summ += (num-get_min_num(num_len))*num_len
    return summ


def are_equivalent(num, segment):
    if len(num) != len(segment):
        return False
    for i in range(0, len(digit_list)):
        if num_list[i] != digit_list[i] and digit_list[i] != 'x':
            return False
    return True


def extra_segments(old_segments, border, shift):
    entire_string = ''
    i = 0
    while old_segments[i] != border:
        entire_string += old_segments[i]
        i += 1
        if i == len(old_segments):
            return [float('Inf'), 0]
    new_segments = to_segment(entire_string, len(border)-1, shift)
    for k in range(i, len(old_segments)):
        new_segments.append(old_segments[k])
    return min_num_in_segments(new_segments)



def min_num_in_segments(segments):
    if segments[0][0] is '0':
        return [float('Inf'), 0]
    if len(segments) is 1:
        if segments[0][0] is 'x' and segments[0][-1] is 'x':
            return [float('Inf'), 0]
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
                return [str(int(filled)-len(segments)+1),
                        num_of_crosses(segments[0])]
    return [float('Inf'), 0]


def min_num_in_extra_segments(segments):
    nums = dict()
    if len(segments[0]) > 1:
        for shift in range(0, len(segments[0])):
            extra = extra_segments(segments,
                           str(min_num_to_fill(len(segments[0]), 'l')),
                           shift)
            if extra[0] != float('Inf'):
                nums[int(extra[0])] = extra
    min_num = min_num_in_segments(segments)
    if min_num[0] != float('Inf'):
                nums[int(min_num[0])] = min_num
    if len(nums.keys()) > 0:
        best_num = int(min(nums.keys()))
        return nums[best_num]
    else:
        return [float('Inf'), 0]


def split_seq(str_seq):
    nums = dict()
    for segment_len in range(1, len(str_seq)+1+num_of_zero(str_seq)):
        for shift in range(0, segment_len):
            segments = to_segment(str_seq, segment_len, shift)
            min_num = min_num_in_segments(segments)
            if min_num[0] != float('Inf'):
                nums[int(min_num[0])] = min_num[1]
    best_num = int(min(nums.keys()))
    return [best_num, nums[best_num]]


#str_seq = input('Введите искомую последовательность: ')

str_seq = '001'
# todo: fix '8910' bug
print(first100.find(str_seq))
result = split_seq(str_seq)
distance = find_distance(result[0])
print(distance+result[1])

#print(extra_segments(['89', '10'], '10'))
#print(extra_segments(['x79', '899', '100', '101', '102'], '100', 0))

# Тест на глюки:
'''
for i in range(1, 1001):
    print(i, end=' ')
    str_seq = str(i)+str(i+1)+str(i+2)
    result = split_seq(str_seq)
    distance = find_distance(result[0])
    if distance+result[1] != first100.find(str_seq):
        print(str_seq)
'''
print('Готово')
