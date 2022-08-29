import time
import random

key_length = 20

def gen_license():
    number = '0123456789'
    alpha2 = 'abcdefghijklmnopqrstuvwxyz'
    alpha = 'abcdefghijklmnopqrstuvwxyz.+¡*'
    alphaMayus = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-!'
    id = ''
    for i in range(0,key_length,2):
        id += random.choice(alpha2)
        id += random.choice(alphaMayus)
        id += random.choice(number)
        id += random.choice(alpha)
        id += random.choice(alpha)        
    return id

def time_conversion(sec):
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S",ty_res)
    return res