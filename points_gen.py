import os
import string
import math
import random

f = open('points', 'w')
i = 0
points = 50000
while i<=points:
    strW = str(random.randint(-5000, 5000))+','+str(random.randint(-5000, 5000))
    if i < points:
        strW += ' '
    f.write(strW)
    i += 1
f.close()