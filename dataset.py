#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : dataset.py


class ImgInfo(object):
    def __init__(self):
        self.path = ''
        self.width = 0
        self.height = 0
        self.channel = 0


class FeatureData(object):
    def __init__(self):
        self.lmx = []
        self.lmy = []
        self.feature_num = 10
        self.is_hiden = []

    def getFeatNum(self):
        return self.feature_num


class ImageFeatureData(object):
    def __init__(self):
        self.img_info = None
        self.features: list[FeatureData] = []


class TaggingItem(object):
    def __init__(self):
        self.img = ''
        self.tagging_file = ''
