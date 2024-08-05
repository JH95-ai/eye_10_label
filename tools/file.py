#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : file.py

import os
import sys
import json
import cv2

from typing import List

from dataset import ImageFeatureData, TaggingItem


def eachFiles(path):
    files = []
    dirs = os.listdir(path)
    for name in dirs:
        file = path + '/' + name
        if os.path.isfile(file):
            items = os.path.splitext(file)
            if items[1] == ".jpg" or items[1] == ".JPG" or items[1] == ".png" or items[1] == ".jpeg":
                # print(path)
                files.append(file)
        else:
            eachFiles(file)
    return files


def saveFeatureResult(data: ImageFeatureData, output):
    if data and data.img_info and len(data.features) > 0:
        info = data.img_info
        src_path = os.path.dirname(info.path)
        src_name = os.path.basename(info.path)
        print("path: %s name: %s" % (src_path, src_name))
        out_file = os.path.join(output, src_name.split('.')[0] + ".json")
        print("output: %s" % out_file)
        width = info.width
        height = info.height
        print("width:%d, height:%d" % (width, height))
        feature = data.features[0]
        if len(feature.lmx) != feature.getFeatNum() and len(feature.lmy) != feature.getFeatNum():
            num_x = len(feature.lmx)
            num_y = len(feature.lmy)
            print("warning: the features is not match 26(%d,%d)!" % (num_x, num_y))
        options_val = {"imgWidth": width, "imgHeight": height}
        features = []
        for i in range(len(feature.lmx)):
            x = feature.lmx[i]
            y = feature.lmy[i]
            title_txt = '1-' + str(i + 1)
            point_prop = {"formData": {"prifixId": 1, "id": i + 1, "pointType":  feature.is_hiden[i]}}
            feature_val = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]},
                           "properties": point_prop, "title": title_txt}
            features.append(feature_val)
        markResult = {"type": "FeatureCollection", "features": features}
        output_json = {"markResult": markResult, "property": "", "options": options_val}
        data = json.dumps(output_json, indent=3)
        with open(out_file, 'w') as file:  # 设置文件对象
            file.write(data)


def readFeatureResult(file):
    json_data = None
    feature_x = []
    feature_y = []
    feature_type = []
    with open(file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    # print(json_data)
    mark = json_data["markResult"]
    info = json_data["options"]
    width = info["imgWidth"]
    height = info["imgHeight"]

    features = mark["features"]
    for feat in features:
        geometry = feat["geometry"]
        coord = geometry["coordinates"]
        properties = feat["properties"]
        formData = properties["formData"]
        pointType = formData["pointType"]

        x = coord[0]
        y = coord[1]
        feature_x.append(x)
        feature_y.append(y)
        feature_type.append(pointType)
    return feature_x, feature_y, feature_type


tItemList = List[TaggingItem]
fileList = List[str]


def readDoTaggingFile(file):
    json_data = None
    with open(file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    data = []
    for item in json_data:
        img = item["img"]
        tag_file = item["tagging"]
        one = TaggingItem()
        one.img = img
        one.tagging_file = tag_file
        data.append(one)
    return data


def writeDoTaggingFile(file, data: tItemList):
    output_json = []
    for tItem in data:
        # print("item: ", tItem)
        item = {"img": tItem.img, "tagging": tItem.tagging_file}
        output_json.append(item)

    data = json.dumps(output_json, indent=3)
    with open(file, 'w') as f:  # 设置文件对象
        f.write(data)


def createDoTaggingList(data: fileList):
    do_list = []
    for file in data:
        # print("", file)
        item = TaggingItem()
        item.img = file
        item.tagging_file = ''
        do_list.append(item)
    return do_list
