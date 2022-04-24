import math


def int_to_bytes(num):
    length = math.ceil(math.log(num)/math.log(256))
    return num.to_bytes(length, 'big')
