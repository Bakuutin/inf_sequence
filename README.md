# Infinite sequence
Программа находит первое вхождение введённой последовательности в последовательность,
полученную склейкой всех натуральных чисел
***


Пример работы программы:

    Введите искомую последовательность: 6789
    Ответ: 6

Ещё пример:

    Введите искомую последовательность: 101
    Ответ: 10

И ещё. Рассмотрим случай, когда когда рассматриваемая последовательность столь длинная, что в ней встречается сразу несколько границ порядков:

    Введите искомую последовательность: 456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101
    Ответ: 4

И вот ещё пример:

    Введите искомую последовательность: 7965400
    Ответ: 26944648

Одни нули подряд:

    Введите искомую последовательность: 000
    Ответ: 2891

А вот график, на котором зачение по оси ординат соответствует расстоянию до первого вхождения str(x):
![Я использовал matplotlib](https://raw.githubusercontent.com/Bakuutin/inf_sequence/master/dispersion.svg)
_кликабельно, вектор_
