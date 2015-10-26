# -*- coding: utf8 -*-
import os

# Словарь значений для систем счисления до 16-ричной
dicta = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']

# Ситаем построчно из файла. Принимаем в расчёт большие объёмы
def readFileByLine(fileName):
    with open(fileName, 'r') as f:
        for line in f:
            # Убираем символы перевода строки и отправляем в рассчёт
            calc(line.strip("\r,\n"))

#
# Непосредственный пересчёт в нужную систему счисления
#
# Входные данные
#   floatVal - число для пересчёта
#   basis    - основание системы счисления
#
# Выходные данные
#   floatVal в basis системе счисления
#
def radix(floatVal, basis):
    # Разделяем целую и дробную части
    integer = int(floatVal)
    floatVal = floatVal-integer
    # Сложим сюда переведённые части и потом соединим
    converted = dict();
    
    # Пересчитываем целую часть
    if integer:
        # Здесь запоминаем остатки от деления
        convertedInt = []
        # Поехали делить
        while True:
            # Выйдем из цикла когда делить будет уже нечего
            if integer<basis:
                # но запомним остаток
                convertedInt.append(integer)
                break
            # Остаток деления
            residue = integer%basis
            # Для дальнейшего деления
            integer = (integer-residue)/basis
            # Записываем остаток
            convertedInt.append(dicta[residue])
        # Нам нужен обратный порядок следования
        convertedInt[::-1]
        converted['int'] = ''.join(map(str, convertedInt))
    else:
        # Нет целого части
        converted['int'] = '0'
    
    # Пересчитываем дробную часть
    if floatVal:
        # Запоминаем значения после рассчётов
        converted['float'] = []
        # Здесь будем отдельно проверять период
        check = []
        # И строчка куда будет записан период для дальнейшего присоединения
        period = ''
        while True:
            # Закончили пересчёт
            if floatVal == 0:
                break
            # Ищем значение
            floatVal = floatVal*basis
            # Мы либо наткнулись на период
            try:
                # Откуда начался этот период, он может быть и 8.9(4), и 4.34(183), и т.д.
                position = check.index(str(floatVal))
                # Срез: здесь период
                check = converted['float'][position:]
                # Срез: здесь до переода его мы запишем в коннечной склейке целой и дробной части, как и период
                converted['float'] = converted['float'][:position]
                # Вот наш переод
                period = '('+''.join(map(str, check))+')'
                break
            # Либо нет
            except ValueError:
                # Зтслеживаем период
                check.append(str(floatVal))
                # Записывааем значения
                residue = int(floatVal)
                # Нам нужно целое число
                floatVal = floatVal-residue
                converted['float'].append(dicta[residue])
            
            # Дробная часть может и не закончится, так что ограничим точность до 50 знаков после запятой
            if len(check)==50:
                break
        # Склеим наши части
        converted['float'] = '.'+''.join(map(str, converted['float']))+period
    else:
        converted['float'] = ''
    # Целая + дробная
    return converted['int']+converted['float']

#
# Проверяем данные
# Высчитываем результат деления
# Отправляем на пересчёт
#
# Входные параметры
#   line - строка
#
def calc(line):
    if line:
        # Зазделим на значения
        numbers = line.split(' ')
        # Только 3 значения
        if len(numbers) != 3:
            printErrors('Не хватает данных для рассчёта', line)
        else:
            # Точлько целые числа
            try:
                a = int(numbers[0])
                b = int(numbers[1])
                k = int(numbers[2])
                # Делить на 0 нельзя, систему счисления 1 пропускаем
                if b == 0:
                    printErrors('Делить на 0 нельзя', line)
                # Не больше 16 систем счисления
                elif k > 16 or k == 1 or k == 0:
                    printErrors('Некорректная система счисления', line)
                # Всё ок
                else:
                    print radix(float(numbers[0])/float(numbers[1]), int(numbers[2]))
            except ValueError:
                printErrors('Найдены некорректные значения', line)

#
# Пишем сообщения
#
def printErrors(msg, line=''):
    if line:
        line = ' (cтрока "'+line+'")'
    print(msg+line)


# Тело
print('Инициализация входных данных')
# Файл с данными
fileName = 'radix'
if os.path.exists(fileName):
    readFileByLine(fileName)
# Или читаем с консоли пока сами не захотим выйти
else:
    print ('Введите 2 числа и систему счисления через пробел (формат: a b c). Для выхода введите ":q"')
    while True:
        line = raw_input()
        if line == ':q':
            break
        # Отправляем на пересчёт введённые значения
        calc(line)