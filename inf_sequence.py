"""
Находит первое вхождение введённой последовательности в последовательность,
полученную склейкой всех натуральных чисел
"""

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


def min_num_to_fill(num_of_crosses, side='l'):
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


def to_segment(str_seq, segment_len, shift=0):
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
    for i in range(0, len(segment)):
        if num[i] != segment[i] and segment[i] != 'x':
            return False
    return True


def del_ranks_border(segments):
    try:
        max_num_index = segments.index(str(max_num_to_fill(len(segments[0]))-1))
        # Ищем сегмент, заполненный девятками
        # Например, '99' или '99999
        new_len = len(segments[0])+1
        tail = ''
        while len(segments) > max_num_index+1:
            tail += segments.pop(max_num_index+1)
        tail_segments = to_segment(tail, new_len)
        del_ranks_border(tail_segments) # Рассматриваем случай, когда рассматриваемая последовательность столь длинна
                                        # что в ней встречается сразу несколько границ порядков, например:
        segments.extend(tail_segments)  # "89101112...9899100101102" или даже "9899100101102...99899910001001"
    except ValueError:
        try:
            min_num_index = segments.index(str(min_num_to_fill(len(segments[0]))))
            # Ищем сегмент, младшее число в порядке
            # Например, '10' или '10000' в зависимости от длины сегмента
            if min_num_index != 0:
                new_len = len(segments[0])-1
                tail = ''
                while len(segments) - min_num_index > 1:
                    tail += segments.pop(0)
                new_segments = to_segment(tail, new_len)
                shift = num_of_crosses(new_segments[-1])
                new_segments = to_segment(tail, new_len, shift)
                del_ranks_border(tail_segments) # Как описано выше, мы проверим, вдруг есть ещё границы порядков
                for segment in new_segments[::-1]: # Вставляем в начало новую голову
                    segments.insert(0, segment)
        except ValueError:
            ... # Мне нравится свобода синтаксиса в третьем питоне


def explore_segments(segments):
    """
    Исследует разбиение из сегмнтов на корректность.
    Если разбиение некорректно, возвращает False,
    иначе возвращает кортеж из полного первого сегмента
    и длинны сдвига, на который этот сегмент отрезан
    """
    if len(segments) is 1 and segments[0][0] is not '0':
        if segments[0][0] is 'x' or segments[0][-1] is 'x':
            # Вообще-то такой сегмент корректен, но мы можем
            # утверждать, что он не наименьший из возможных
            return False
        return int(segments[0]), 0

    del_ranks_border(segments) # Уберём границы порядков, если они есть

    for segment in segments:
        if segment[0] is '0':
            return False

    shift = num_of_crosses(segments[0])

    if segments[0][0] is 'x':
        if len(segments) is 2:
            if segments[1][-1] is not 'x':
                # Если сегмента два, и второй это число
                first_int = int(segments[1])-1
                if are_equivalent(str(first_int), segments[0]):
                    return first_int, shift
                return False
            else:
                # Если сегмента два, и оба неполные. Самый сложный случай.
                if num_of_crosses(segments[0]) <= num_of_crosses(segments[1]):
                    for i in range(min_num_to_fill(num_of_crosses(segments[0]), 'l'),
                                   max_num_to_fill(num_of_crosses(segments[0]))):
                        filled = int(fill_crosses(segments[0], str(i)))
                        if are_equivalent(str(filled+1), segments[1]):
                            return filled, shift
                else:
                    for i in range(min_num_to_fill(num_of_crosses(segments[1]), 'r'),
                                   max_num_to_fill(num_of_crosses(segments[1]))):
                        filled = int(fill_crosses(segments[1], str(i)))
                        if are_equivalent(str(filled-1), segments[0]):
                            return filled-1, shift
                return False
        else:
            # Если сегментов больше двух, то сегменты в середине точно полные.
            # Второй сегмент точно в середине. Возьмём его за точку отсчета.
            first_int = int(segments[1])-1
            for i in range(1, len(segments)):
                if are_equivalent(str(first_int+i), segments[i]) is False:
                    return False
            return first_int, shift

    first_int = int(segments[0])
    for i in range(1, len(segments)):
        if are_equivalent(str(first_int+i), segments[i]) is False:
            return False
    return first_int, shift


def split_seq(str_seq):
    nums = dict()
    for segment_len in range(1, len(str_seq)+1+num_of_zero(str_seq)):
        for shift in range(0, segment_len):
            segments = to_segment(str_seq, segment_len, shift)
            min_num = explore_segments(segments)
            if min_num:
                nums[min_num[0]] = min_num[1]
        if len(nums) > 0:
            best_num = min(nums.keys())
            return [best_num, nums[best_num]]
    return False

str_seq = input('Введите искомую последовательность: ')
print(first100.find(str_seq))
result = split_seq(str_seq)
distance = find_distance(result[0])
print(distance+result[1])