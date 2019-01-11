from PIL import Image
import os
import qrcode
import hashlib
from datetime import datetime

def makeQRcode(student_num, text):
    img = qrcode.make(text)
    img.save('./static/QRcode/' + str(student_num) + '.png')
    img.save('../student/' + str(student_num) + '.png')

def get_hash(student_num):
    text = str(student_num).encode('utf-8')
    hash_value = hashlib.sha512(text).hexdigest()
    return hash_value

