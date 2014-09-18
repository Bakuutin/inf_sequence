"""
Находит первое вхождение введённой последовательности в последовательность,
полученную склейкой всех натуральных чисел
"""


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
    """
    Заполняет строку-шаблон, заменяя
    последовательность из 'x' на число num
    """
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


def min_num_to_fill(len_of_x, side='l'):
    """
    Возвращает минимальное число, которым
    можно заполнить последовательность 'x'
    в сегменте. side показывает сторону,
    где в сегменте стоят 'x'
    """
    if len_of_x is 0 or side is 'r':
        return 0
    else:
        return int('1'+'0'*(len_of_x-1))


def max_num_to_fill(len_of_x):
    """
    Возвращает минимальное число, которым
    можно заполнить последовательность 'x'
    в сегменте.
    """
    if len_of_x is 0:
        return 0
    return int('9'*len_of_x)+1



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
    Делит строку на list из сегментов
    """
    ext_str_seq = segment_len*'x'+str_seq+segment_len*'x'
    segments = [ext_str_seq[num+shift:num+segment_len+shift]
                for num in range(0, len(ext_str_seq), segment_len)
                if not is_empty(ext_str_seq[num+shift:num+segment_len+shift])
                ]
    return segments


def get_rank_size(rank):
    """
    Возвращает количество натуральных чисел,
    имеющих длину rank.
    """
    if rank is 0:
        return 0
    size = '9'
    for i in range(1, rank):
        size += '0'
    return int(size)


def get_min_num(rank):
    """
    Возвращает минимальное число длиной rank цифр
    """
    min_num = '1'
    for i in range(1, rank):
        min_num += '0'
    return int(min_num)


def find_distance(num):
    """
    Находит расстояние до числа num
    в бесконечной последовательности
    """
    summ = 0
    num_len = len(str(num))
    for rank in range(1, num_len):
        summ += rank * get_rank_size(rank)
    summ += (num-get_min_num(num_len))*num_len
    return summ


def are_equivalent(num, segment):
    """
    Проверяет соответствие числа шаблону-сегменту.
    Например: '100' ~ '1xx'
    """
    if len(num) != len(segment):
        return False
    for i in range(0, len(segment)):
        if num[i] != segment[i] and segment[i] != 'x':
            return False
    return True


def del_ranks_border(segments):
    """
    Рекурсивно находит в разбиении границы порядков и
    восстанавливает правильную длину чисел. Например:
    ['98', '99', '10', '01'] → ['98', '99', '100', '1xx']
    """
    try:
        max_num_index = segments.index(str(max_num_to_fill(len(segments[0]))-1))
        # Ищем сегмент, заполненный девятками
        # Например, '99' или '99999
        if max_num_index != len(segments)-1:
            new_len = len(segments[0])+1
            tail = ''
            while len(segments) > max_num_index+1:
                tail += segments.pop(max_num_index+1)
            tail_segments = to_segment(tail, new_len)
            del_ranks_border(tail_segments)  # Рассматриваем случай, когда последовательность столь длинная,
                                             # что в ней встречается сразу несколько границ порядков, например:
            segments.extend(tail_segments)   # "89101112...9899100101102" или даже "9899100101102...99899910001001"
    except ValueError:
        try:
            min_num_index = segments.index(str(min_num_to_fill(len(segments[0]))))
            # Ищем сегмент, младшее число в порядке
            # Например, '10' или '10000' в зависимости от длины сегмента
            if min_num_index != 0:
                new_len = len(segments[0])-1
                if new_len is 0:
                    return
                head = ''
                if len(segments) is 2 and min_num_index is 1:
                    head += segments.pop(0)
                while len(segments) - min_num_index > 1:
                    head += segments.pop(0)
                if len(head) is 0:
                    return
                head_segments = to_segment(head, new_len)
                shift = num_of_crosses(head_segments[-1])
                head_segments = to_segment(head, new_len, shift)
                del_ranks_border(head_segments)  # Как описано выше, мы проверим, вдруг есть ещё границы порядков
                for segment in head_segments[::-1]:  # Вставляем в начало новую голову
                    segments.insert(0, segment)
        except ValueError:
            ...  # Мне нравится свобода синтаксиса в третьем питоне


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
            # утверждать, что он не наименьший из возможных,
            # кроме случаев вида 'x0000'
            if segments[0][0] == 'x':
                for digit in segments[0][1:]:
                    if digit != '0':
                        return False
                return get_min_num(len(segments[0])), 1  # Сдвиг, в этом случае, всегда 1
            return False                                 # т.к. 'x' в начале только один
        return int(segments[0]), 0

    del_ranks_border(segments)  # Уберём границы порядков

    for segment in segments:
        #  Ни одно число не начинается с нуля
        if segment[0] is '0':
            return False

    shift = num_of_crosses(segments[0])  # Вычислим, сколько отрезано символов от начала
                                         # первого числа, чтобы позже правильно сосчитать
    if segments[0][0] is 'x':            # расстояние до первого вхождения
        if len(segments) is 2:
            if segments[1][-1] is not 'x':
                # Если сегмента два, и второй это число
                first_int = int(segments[1])-1
                if are_equivalent(str(first_int), segments[0]):
                    return first_int, shift
                return False
            else:
                # Если сегмента два, и оба неполные. Самый сложный случай.
                # Перебором подставляем цифры в тот сегмент, где пропусков меньше
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
            for i in range(0, len(segments)):
                if are_equivalent(str(first_int+i), segments[i]) is False:
                    return False
            return first_int, shift

    # Сюда доходят только такие разбиения, в которых первый сегмент натуральное число
    # Последовательно проверяем сегменты оставшегося хвоста
    first_int = int(segments[0])
    for i in range(1, len(segments)):
        if are_equivalent(str(first_int+i), segments[i]) is False:
            return False
    return first_int, shift


def split_seq(str_seq):
    """
    Перебирает возможные разбиения строки, пока не найдёт корректное
    Если таковых находится несколько, выбирает то, расстояние до которого меньше
    Возвращает кортеж из числа, которому соответствует первый сегмент корректного разбиения
    и длинны сдвига, на который этот сегмент отрезан
    """
    nums = dict()
    for segment_len in range(1, len(str_seq)+1+num_of_zero(str_seq)):
        # Максимальная возможная длина сегмента в разбиении
        # зависит не только от длины строки, но и от количества нулей
        # в её начале. Например, '00' → ['100']
        for shift in range(0, segment_len):
            segments = to_segment(str_seq, segment_len, shift)
            min_num = explore_segments(segments)
            if min_num:
                if min_num[0] in nums.keys():
                    if min_num[1] < nums[min_num[0]]:
                        nums[min_num[0]] = min_num[1]
                else:
                    nums[min_num[0]] = min_num[1]
        if len(nums) > 0:
            # Если для текущей длины разбиения уже найден ответ,
            # поиск можно прекратить, дальнейшие корректные разбиения
            # всё равно не будут наилучшими
            best_num = min(nums.keys())
            return best_num, nums[best_num]
    return False


def show_answer(str_seq):
    """
    Выводит ответ в человекочитаемом виде
    """
    result = split_seq(str_seq)
    distance = find_distance(result[0])
    print('Ответ: {}'.format(distance+result[1]+1))


str_seq = input('Введите искомую последовательность: ')
show_answer(str_seq)
