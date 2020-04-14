# !/usr/bin/env python
# -*- coding: utf8 -*-
# 
#

"""
@author: jiangshuai
@file: caption_api.py
@time: 2020/4/13 19:05
@desc: 图片描述api
"""
import caption
import torch
import os
import sys
import json
import logging
import baidu.agc.base.baidu_translate as baidu_translate


g_cur_path = os.path.dirname(os.path.abspath(__file__)) + '/'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_file = g_cur_path + 'model/BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar'
word_map_file = g_cur_path + 'data/WORDMAP_coco_5_cap_per_img_5_min_word_freq.json'
# Load model
checkpoint = torch.load(model_file, map_location=str(device))
decoder = checkpoint['decoder']
decoder = decoder.to(device)
decoder.eval()
encoder = checkpoint['encoder']
encoder = encoder.to(device)
encoder.eval()

# Load word map (word2ix)
with open(word_map_file, 'r') as j:
    word_map = json.load(j)
rev_word_map = {v: k for k, v in word_map.items()}  # ix2word


def main_image_caption(image_file, beam_size=5, dont_smooth=''):
    """
    图片描述生成，调用脚本
    :param image_file: 本地文件的uri，或者图片的url
    :return:
    """
    logging.info('get a new query\t{}'.format(image_file))
    res = {'en': '', 'zh': ''}
    # Encode, decode with attention and beam search
    seq, alphas = caption.caption_image_beam_search(encoder, decoder, image_file, word_map, beam_size)
    alphas = torch.FloatTensor(alphas)
    # 打印image2text结果，翻译成中文
    words_l = [rev_word_map[ind] for ind in seq]
    en_words = ' '.join(words_l[1: -1])
    bdt = baidu_translate.BaiDuTranslate()
    zh_word_dict = bdt.translate(en_words, 'en', 'zh')
    zh_words = zh_word_dict['trans_result'][0]['dst']
    res['en'] = en_words
    res['zh'] = zh_words
    logging.info('return a caption\t'.format(json.dumps(res, ensure_ascii=False)))
    return res


if __name__ == '__main__':
    main_image_caption('http://agc-demo.gz.bcebos.com/image2text/test1.jpg')
