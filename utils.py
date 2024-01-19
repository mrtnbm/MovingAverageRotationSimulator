import math

def factor_to_percentage(factor):
    return str(round((factor - 1) * 100, 2)) + '%'

def floor2(value):
    return math.floor(value * 100) / 100