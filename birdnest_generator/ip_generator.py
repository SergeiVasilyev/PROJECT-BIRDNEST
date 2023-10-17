import random
import uuid

def get_random_mac():
    ipv4 = ''
    for n in range(6):
        ipv4 += uuid.uuid4().hex[:2] + ':'
    return ipv4[:-1]

def get_random_ipv4():
    ipv4 = ''
    for n in range(4):
        ipv4 += str(random.randint(0, 255)) + '.'
    return ipv4[:-1]

def get_random_ipv6():
    ipv6 = ''
    for n in range(8):
        ipv6 += uuid.uuid4().hex[:4] + ':'
    return ipv6[:-1]

