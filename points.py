# -*- coding: utf8 -*-
import os
import string
import math

#
# Читаем данные
#
# Выходные данные
#   массив с координатами точек
#
def inp():
    print('Определение точек на плоскости')
    # Файл с данными
    fileName = 'points'
    if os.path.exists(fileName):
        # Для Big Data лучше бы использовать поэтапное чтение из файла кусками. Могу рассказать как бы это реализовал на следующем этапе )
        f = open(fileName, 'r')
        points = f.read()
        print('Координаты взяты из файла "'+fileName+'"')
        f.close()
    # Консольный ввод
    else:
        # Вводим все координаты в дну строку. Можно было бы сделать и поэтапным ввод
        points = raw_input('Введите координаты точек (формат: x1,y1 x2,y2 ...): ')
    # Очищаем от пробелов
    points = points.strip()
    # и разбиваем на точки с координатами
    mass = points.split(' ')
    # Нам нужны как минимум 2 точки
    if len(mass) == 1:
        print('Нужно задать как минимум 2 точки')
        # Прерываемся
        return

    return mass

#
# Создаём карту точек
#
# Входные данные
#   points - координаты точек
#
# Выходные данные
#   карта точек с целочисленными координатами и расстоянием от центра плоскости
#   по которым будем определять близость точек дрг к другу
#
def mapping(points):
    if len(points):
        # Карта
        map = dict()
        # Точки на карте (с координатами)
        map['points'] = dict()
        # Расстояние от центра плоскости до точки
        distance = []
        # Пронумеруем точки
        index = 0
        # Пройдёмся по ним и посчитаем расстояния и созданим карту
        for point in points:
            # Не забываем про нумерацию
            index += 1
            # Получаем координаты
            coord = point.split(',')
            # Мы рассматриваем двумерную систему координат
            if len(coord) == 2:
                try:
                    # Работаем с чсилами
                    x = int(coord[0])
                    y = int(coord[1])
                    # Расстояние до центра плоскости
                    c = math.sqrt(math.pow(x, 2)+math.pow(y, 2))
                    # Обновим данные по расстояниям
                    append = (index, c)
                    distance.append(append)
                    # и запишем данные в карту точек
                    map['points'][index] = dict()
                    map['points'][index]['x'] = x
                    map['points'][index]['y'] = y
                except ValueError:
                    # У точки координаты не числа?
                    print('Ошибка инициализации координат у точки "'+point+'"')
                    return
            else:
                print('Ошибка перечисления координат у точки "'+point+'"')
                return
        # Для лёгкого поиска соседей у точки, отсортируем расстояния от точки до центра плоскости
        distance = sorted(distance, key=lambda x: x[::-1])
        # и добавим эту информацию в карту
        map['distance'] = distance
        
        return map

#
# Рассчитываем расстояния между точками.
#
# Взодные данные
#   a - 1-ая точка
#   b - 2-яа точка
#   coord - возьмём координаты для точке
#   distanceMap - пул расстояний между точками
#     Расстояние от a до b тоже самое, что и от b до a
#
# Выходные данные
#   Расстояние от a до b
#
def distanceBetweenPoints(a, b, coord, distanceMap):
    # создадим индекс определяющий пару точек
    index = [a, b]
    # 12 и 21 одно и тоже => приведём всё к единому виду
    index.sort()
    indexStr = ''.join(map(str, index))
    
    # Расстояние уже посчитано
    if distanceMap.has_key(indexStr):
        return distanceMap[indexStr]
    else:
        # Считаем расстояние
        # Координаты
        cax = coord[a]['x'];
        cbx = coord[b]['x'];
        cay = coord[a]['y'];
        cby = coord[b]['y'];
        # Считаем стороны прямоугольного треугольника с участием этих точек
        # Одна сторона
        # Точки находятся в одно четверти
        if cax > 0 and cbx > 0 or cax < 0 and cbx < 0:
            x = math.fabs(cax - cbx)
        # или в разных
        else:
            x = math.fabs(cax) + math.fabs(cbx)
        # Тоже самое для второй стороны
        if cay > 0 and cby > 0 or cay < 0 and cby < 0:
            y = math.fabs(cay - cby)
        else:
            y = math.fabs(cay) + math.fabs(cby)

        # Точки на одной оси
        if x == 0:
            distance = y
        elif y == 0:
            distance = x
        else:
            distance = math.sqrt(math.pow(x, 2)+math.pow(y, 2))
        # Запомним расстояния между точками
        distanceMap[indexStr] = distance

        return distance

# Ввод
points = inp()
# Что-то есть на входе
if points:
    # Нужно быдет для цикла в котором буду перебирать значения расстояния до центра,
    # определяя какая точка ближе. Т.к. нумерация с нуля, то минусуем 1
    lenPointsForCircle = len(points) - 1
    
    # Получаем карту точек
    pointsMap = mapping(points)
    if pointsMap:
        # Расстояние между точками.
        distanceBetweenPointsList = dict()
        index = 0
        # Расстояния отсортированны. Начнём от центра плоскости
        for distance in pointsMap['distance']:
            # Определяем ближайшую точку
            #   у конечной это предыдущая, у остальных сравниваем разницу расстояний с соседями (в этом условии выбираем предудущую)
            if index == lenPointsForCircle or distance[1] - pointsMap['distance'][index-1][1] < pointsMap['distance'][index+1][1] - distance[1] and index != 0:
                nearestPoint = pointsMap['distance'][index-1]
            # Для начальной точки ближайшая вторая и для непоходящих под первое условие ближняя - это следующая точка
            else:
                nearestPoint = pointsMap['distance'][index+1]
            # Поссчитаем расстояние до ближайшей точки
            distanceToNearestPoint = distanceBetweenPoints(distance[0], nearestPoint[0], pointsMap['points'], distanceBetweenPointsList)
            # Увеличим в 2 раза
            distanceToNearestPoint *= 2;
            # Соседи
            nearberhoods = []
            # Пройдёмся по расстояниям до других точек
            for point in pointsMap['points']:
                # Исключая себя
                if point != distance[0]:
                    # Расстояние
                    calcDistance = distanceBetweenPoints(distance[0], point, pointsMap['points'], distanceBetweenPointsList)
                    #  Походит в качестве соседа?
                    if calcDistance <= distanceToNearestPoint:
                        # Да
                        nearberhoods.append('('+str(pointsMap['points'][point]['x'])+','+str(pointsMap['points'][point]['y'])+')')
            # Напишем результат
            collect  = 'Координаты соседних от ('+str(pointsMap['points'][distance[0]]['x'])+','+str(pointsMap['points'][distance[0]]['y'])+') точек: '
            collect += ', '.join(map(str, nearberhoods))
            print(collect)
            # Дальше
            index += 1