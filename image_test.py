#!/usr/bin/env python
# coding: utf-8


import os
from PIL import Image


def image_resize(image_name='', width='', hight=''):
    global msg
    try:
        img_path = (os.path.join(os.path.expanduser("~"), 'Desktop'))
        print(img_path)
        a = os.path.join(img_path, image_name)
        img = Image.open(a)
        resize = img.resize((int(width), int(hight)), Image.ANTIALIAS)
        resize.save(a)
        # print(resize.size)
        msg = '%s 調整大小成功' % image_name
        return msg
    except FileNotFoundError as e:
        msg = ('%s檔案不存在' % image_name)
        return msg
    # return img_path
