import time
from cmu_112_graphics import *

def name():
    return 1/0


try:
    name()
    print(1)
except:
    raise Exception("You got an errror!")
