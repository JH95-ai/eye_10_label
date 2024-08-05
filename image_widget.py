#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : image_widget.py

import os
import math
import threading

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter , QPen
from PyQt5.QtCore import Qt,QPoint
import image_view

# import model.landmark as engine
import dataset
import tools.file as FileTool
# import mediapipe as mp
import cv2
class ImageWidget(QWidget):
    onUIUpdated = pyqtSignal(int)
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.engine = engine.LMEngine()

        # pwd = os.getcwd()
        # self.head_model = pwd + '/model/head_detector.pb'
        # self.lm_model = pwd + '/model/landmarks.pb'
        # print("head model: ", self.head_model)
        # print("lm model: ", self.lm_model)
        # self.engine.init(self.head_model, self.lm_model)
        # self.eye_index_list =[33,160,159,157,133,154,145,163,#mediapipe left_eye index
        #                       382,384,386,387,263,390,374,380,#mediapipe right_eye index
        #                       469, 470, 471, 472,#mediapipe left_iris index
        #                       474, 475, 476, 477 #mediapipe right_iris index
        #                       ]
        #
        # self.currentImgFeature = None
        # mp_face_mesh = mp.solutions.face_mesh

        # self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True,
        #                                         max_num_faces=1,
        #                                         refine_landmarks=True,
        #                                         min_detection_confidence=0.5)
        self.centerLayout = QHBoxLayout(parent)
        self.setLayout(self.centerLayout)
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.image_view = image_view.ImageView()

        self.centerLayout.addWidget(self.image_view)

        # connect
        self.image_view.onScaleFactorChanged.connect(self.onScaleFactorChanged)
        # self.image_view.connectNotify()
        self.start = None
        self.end = None
    def updateImage(self, file):
        self.currentImgFeature = None
        self.image_view.showImage(file)

    # def preloadFeatures(self, file):
    #     if self.currentImgFeature and self.currentImgFeature.file == file:
    #         self.showAllFeatures()
    #     else:
    #         self.removeAllFeatures()
    #         self.image_view.showImage(file)
    #         img = cv2.imread(file)
    #         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         results = self.face_mesh.process(img_rgb)
    #         lmx = []
    #         lmy = []
    #         point_flag = []
    #         if results.multi_face_landmarks:
    #             for face_landmarks in results.multi_face_landmarks:
    #                 # 处理每个人脸的关键点信息
    #                 for i in range(len(self.eye_index_list)):
    #                     x = int(face_landmarks.landmark[self.eye_index_list[i]].x * img.shape[1])
    #                     y = int(face_landmarks.landmark[self.eye_index_list[i]].y * img.shape[0])
    #                     # 处理每个关键点的坐标值
    #                     pointflag = 0
    #                     lmx.append(x)
    #                     lmy.append(y)
    #                     point_flag.append(pointflag)
    #             lmx.insert(19,int((lmx[16]+lmx[18])/2))
    #             lmx.insert(25,int((lmx[21]+lmx[23])/2))
    #             lmy.insert(19,int((lmy[16]+lmy[18])/2))
    #             lmy.insert(25,int((lmy[21]+lmy[23])/2))
    #
    #             point_flag.append(0)
    #             point_flag.append(0)
    #             # lm_x, lm_y = self.engine.run(file)
    #             self.image_view.refreshKeyNode([lmx, lmy,point_flag])
    #             self.showAllFeatures()
    #             self.currentImgFeature = dataset.ImageFeatureData()
    #             self.currentImgFeature.file = file
    #             feature_data = dataset.FeatureData()
    #             feature_data.lmx = lmx
    #             feature_data.lmy = lmy
    #             self.currentImgFeature.features.append(feature_data)
    #         else:
    #             self.showAllFeatures()
    def updateTaggingData(self, file):
        if not os.path.exists(file):
            print("file %s is not exist!" % file)
            return
        feat_x, feat_y, pointType = FileTool.readFeatureResult(file)
        self.image_view.refreshKeyNode([feat_x, feat_y, pointType])

    def showAllFeatures(self):
        self.image_view.hideShowNode(True)

    def hideAllFeatures(self):
        self.image_view.hideShowNode(False)

    def removeAllFeatures(self):
        self.image_view.clearAllNode()

    def removeSelectFeatures(self):
        self.image_view.removeSelectNode()

    def changeInSelectFeaturesToHiden(self):
        self.image_view.changeSelectNodeStatus(1)

    def changeInSelectFeaturesToMiss(self):
        self.image_view.changeSelectNodeStatus(2)

    def changeInSelectFeaturesToNormal(self):
        self.image_view.changeSelectNodeStatus(0)

    def saveResult(self, output):
        print("save_result")
        datas = self.image_view.collectFeatureData()
        if datas and len(datas.features) > 0 and len(datas.features[0].lmx) == 10 and len(datas.features[0].lmy) == 10:
            FileTool.saveFeatureResult(datas, output)
            return True
        else:
            button = QMessageBox.warning(self, "Warning", "Fail, the total number keys is not 10!",
                                         QMessageBox.Ok)
            return False

    def setZoomLevel(self, level):
        step = level - 11
        base = image_view.ZOOM_IN_STEP
        if step < 0:
            base = image_view.ZOOM_OUT_STEP
        factor = 1.0 * math.pow(base, math.fabs(step))
        self.image_view.setScaleFactor(factor)

    def getZoomLevel(self):
        dFactor = self.image_view.getScaleFactor()
        base = image_view.ZOOM_IN_STEP
        if dFactor < 1.0:
            base = image_view.ZOOM_OUT_STEP
        step = math.ceil(math.log(math.fabs(dFactor)) / math.log(base))
        if dFactor > 1.0:
            return step + 11
        else:
            return 11 - step

    def zoomIn(self):
        self.image_view.zoomIn()

    def zoomOut(self):
        self.image_view.zooOut()

    def onScaleFactorChanged(self, factor):
        # print("onScaleFactorChanged ", factor)
        self.onUIUpdated.emit(self.getZoomLevel())

    def setDisplayFeaturesIds(self, flag):
        self.image_view.setDisplayFeaturesIds(flag)

    def setFeatureColor(self, color):
        self.image_view.setNodeColor(color)

    def draw_oval(self):
        self.image_view.draw_oval_image_view()

    def draw_occlusion_oval(self):
        self.image_view.draw_occlusion_view()

    def draw_self_occlusion_oval(self):
        self.image_view.draw_self_occlusion_view()
