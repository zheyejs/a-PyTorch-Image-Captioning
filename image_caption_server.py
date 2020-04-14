# !/usr/bin/env python
# -*- coding: utf8 -*-
#
#

"""
@author: jiangshuai
@file: image_caption_server.py
@time: 2020/4/13 17:35
@desc: image_caption rpc服务
"""

import sys
import os
from baidu.kgx.base.zero_server import ZeroRpcServer
from caption_api import main_image_caption


def main():
    """主程序"""
    #create server
    port = '8008'
    client_url = "tcp://0.0.0.0:" + port
    server = ZeroRpcServer(url_client=client_url)
    #鉴权装饰器，需要传入服务名进行服务级别鉴权
    # service_name = 'event_belong_cls'
    #server func
    worker_num = 1
    server.register_function(main_image_caption)
    server.start(num_threads=worker_num)


if __name__ == '__main__':
    main()
