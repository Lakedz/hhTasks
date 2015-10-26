import os
import string
import random

f = open('radix', 'w')
i = 0
while i<5000000:
    strW = str(random.randint(0, 5000))+' '+str(random.randint(1, 5000))+' '+str(random.randint(2, 16))+"\r\n"
    f.write(strW)
    i += 1
f.close()