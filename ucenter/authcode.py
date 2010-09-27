#!/usr/bin/env python
# coding: utf-8
from hashlib import md5
import base64
from time import time
_auth_key = '25u70bday6U9NaB3va3aC9V4W90er7dfRdV344s7z631c34b09ic6aNca3Sf3b8f'

def auth_code(string = '', operation = 'DECODE', key = '', expiry = 0):
    ckey_length = 4
    if not key: key = _auth_key
    key = md5(key).hexdigest()
    keya = md5(key[:16]).hexdigest()
    keyb = md5(key[16:]).hexdigest()
    if ckey_length:
        if operation == 'DECODE':
            keyc = string[:ckey_length]
        else:
            keyc = md5(str(time())).hexdigest()[-ckey_length:]
    else:
        keyc = ''
    cryptkey = keya + md5(keya + keyc).hexdigest()
    key_length = len(cryptkey)
   
    if operation == 'DECODE':
        string = base64.urlsafe_b64decode(string[ckey_length:])
    else:
        if expiry: expiry = expiry + time()
        expiry = '%010d' % expiry
        string = expiry + md5(string + keyb).hexdigest()[:16] + string
    string_length = len(string)
   
    result = ''
    box = range(256)
    rndkey = {}
    for i in range(256):
        rndkey[i] = ord(cryptkey[i % key_length])
   
    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp
    a = 0
    j = 0
    for i in range(string_length):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))
    if operation == 'DECODE':
        if result[:10] == 0 or int(result[:10]) - time() > 0 or result[10:26] == md5(result[26:] + keyb).hexdigest()[:16]:
            return result[26:]
        else:
            return ''
    else:
        return keyc + base64.urlsafe_b64encode(result) #replace('=', '')

str1 = '1\thqman'
encode_str = auth_code(str1, 'ENCODE') #加密
print encode_str
print auth_code(encode_str) #解密