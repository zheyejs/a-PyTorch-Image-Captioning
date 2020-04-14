# !/usr/bin/env python
# -*- coding: utf8 -*-
# 
#

"""
@author: jiangshuai
@file: image_caption_client.py.py
@time: 2020/4/14 14:20
@desc: 
"""
from baidu.kgx.base.zero_client import ZeroRpcClient

if __name__ == '__main__':
    address = 'tcp://{}'.format('172.18.190.108:8008')

    client = ZeroRpcClient(address, timeout=5)
    result = client.main_image_caption('http://agc-demo.gz.bcebos.com/image2text/test1.jpg')
    print(result)
