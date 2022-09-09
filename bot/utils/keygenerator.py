import time
import random

key_length = 50

def check_key(key):
    global sc
    sc = 0
    check_digit = key[2]
    check_digit_count = 0
    
    for char in key:
        if char == check_digit:
            check_digit += '1'
        sc += ord(char)
    
    if sc > 1700 and sc < 1900:
        return True
    else:
        return False

def gen_key():
    number = '0123456789'
    alpha2 = 'abcdefghijklmnopqrstuvwxyz-'
    alpha = 'abcdefghijklmnopqrstuvwxyz.'
    alphaMayus = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''
    while len(key) < key_length:
        key += random.choice(alphaMayus)
        key += random.choice(alpha)
        key += random.choice(alpha2)
        key += random.choice(number)
    key = key[:-1]
    return key

def gen_license():
    key = gen_key()
    
    if check_key(key):
        pass
    else:
        while check_key == False:
            key = gen_key()
    
    return key

def time_conversion(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S",ty_res)
    return res

"""
license_ = gen_license()
print(license_)"""
