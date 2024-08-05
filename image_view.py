#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : image_view.py

import os
import numpy as np
import math
import cv2

from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, \
    QGraphicsSceneDragDropEvent, QGraphicsSceneMouseEvent, QApplication,QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QImage, QColor, QMouseEvent, QPainter, QTransform, QPen, QDragEnterEvent, \
    QDragLeaveEvent, QFontMetrics, QBrush, QWheelEvent, QFont
from PyQt5 import QtWidgets
from scipy.optimize import least_squares
import image_view
from KeyPointItem import KeyPointItem
from EdgeItem import KeyEdgeItem
from OvalItem import EllipseItem
import dataset
from PyQt5 import QtCore

class ImageItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        QGraphicsPixmapItem.__init__(self, parent)
        self.__flag = 0
        pass

    def flag(self):
        self.__flag

class ImageScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

max_keyPoint_num = 10

max_ellpise_count = 2
max_ellpise_keypoints_num = max_ellpise_count * 5

FONT_SIZE = 12
ZOOM_IN_STEP = 1.25
ZOOM_OUT_STEP = 0.8


class ImageView(QGraphicsView):
    # signal
    onScaleFactorChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        # private variable
        self.__parent = parent
        self.__isMousePress = False
        self.__mousePressPos = None
        self.__keyNum = 0
        self.__keyNodeMap = {}
        self.__edgeMap = {}
        self.__show_image = None
        self.scale_factor = 1.0

        self.__display_ids = True
        self.__show_nodes = True
        self.__node_color = QColor(255, 255, 0)

        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene = ImageScene(parent)
        self.setScene(self.scene)
        self.pixItem = ImageItem(parent)
        self.scene.addItem(self.pixItem)

        self.__hist_flag = 0
        # set Font
        font = QFont()
        self.font_size = FONT_SIZE
        font.setPixelSize(self.font_size)
        self.setFont(font)
        font = self.font()
        size = font.pixelSize()
        print("size: size:", size)

        #self.showImage('/home/ts-liqing/iwork/project/Face/Tool/Facial-Landmarks-Annotation-Tool/example/images/Angelina.jpg')
        # self.start = None
        # self.end = None

        self.start_pos = None
        self.end_pos = None
        self.ellipse_item = None
        self.draw_mode = False
        self.__draw_oval =False
        self.__keyEllipseMap ={}
        self.__keyEllipseflag =[]
        self.pen =None
    def showImage(self, file):
        # self.clearAllNode()
        # self.zoomReset()
        # read image
        if not os.path.exists(file):
            return
        # img = cv2.imread(file)
        img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
        # print("", file, " img:", img)
        height, width = img.shape[:2]
        stride = img.strides
        # Convert to RGB for QImage.
        rgbImg = np.zeros((height, width, 3), np.uint8)
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, rgbImg)
        showImage = QImage(rgbImg.data, width, height, stride[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(showImage)
        #self.pixItem = self.scene.addPixmap(pixmap)
        self.setPixmap(pixmap)
        if self.__show_image is None:
            self.__show_image = dataset.ImgInfo()
        self.__show_image.path = file
        self.__show_image.width = width
        self.__show_image.height = height
        self.__show_image.channel = 3

    def setPixmap(self, pix):
        if self.pixItem is None:
            self.pixItem = ImageItem(self.__parent)
            self.scene.addItem(self.pixItem)
        self.pixItem.setPixmap(pix)
        self.scene.setSceneRect(0, 0, pix.width(), pix.height())

    def getSelectItems(self):
        items = []
        for item in self.scene.selectedItems():
            items.append(item)
        return items

    def getSelectKPItems(self):
        items = []
        for item in self.scene.selectedItems():
            if item.flag() == 1:
                items.append(item)
        return items

    def draw_oval_image_view(self):
        self.__draw_oval = True
        self.__hist_flag = 0
    def draw_occlusion_view(self):
        self.__draw_oval = True
        self.__hist_flag = 1
    def draw_self_occlusion_view(self):
        self.__draw_oval = True
        self.__hist_flag = 2

    def mousePressEvent(self, event: QMouseEvent):
        if self.__draw_oval ==True:
            if event.button() == Qt.LeftButton:
                self.draw_mode = True
                self.start_pos = self.end_pos = self.mapToScene(event.pos())
        else:
            pos = event.pos()  # QPoint
            opos = self.mapToScene(pos)

            self.__isMousePress = True
            self.__mousePressPos = pos
            QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self,event):
        if self.__draw_oval == True and self.draw_mode ==True:
            self.end_pos = self.mapToScene(event.pos())
            self.update_ellipse()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.__isMousePress = False
        pos = event.pos()
        if self.__draw_oval:
            if event.button() == Qt.LeftButton:
                self.draw_mode = False
                self.end_pos = self.mapToScene(event.pos())
                self.update_ellipse()
                new_ell_id = self.getEllipseNodeIndex()
                if new_ell_id is not None:
                    # text_ellpise_count=QtWidgets.QGraphicsTextItem(str(new_ell_id))
                    # text_ellpise_count.setPos(start_pos)
                    # text_ellpise_count.setDefaultTextColor(self.pen)
                    # self.scene.addItem(text_ellpise_count)
                    self.addEllpiseNode(new_ell_id,self.ellipse_item)
                else:
                    print("warning: can not add ellpise node!")
                # ellipse_points_count = len(self.__keyEllipseMap)
                # if ellipse_points_count == max_ellpise_keypoints_num:
                #     self.__keyEllipseMap = {}
                #     ellipse_points_count = 0
                #     self.__keyEllipseflag = []
                # self.get_ellipse_point(start_pos,end_pos,ellipse_points_count,self.__hist_flag,self.__keyEllipseflag)

                self.__draw_oval = False
                self.start_pos = None
                self.end_pos = None
                self.ellipse_item = None
                self.draw_mode = False

        if pos == self.__mousePressPos and (event.button() & Qt.LeftButton) and self.__show_image:
            # step 1: check the mouse presse point is not exist
            isExist, selected = self.pointIsExist(pos)
            if not isExist:
                opos = self.mapToScene(pos)
                self.__keyNum = self.__keyNum + 1
                new_id = self.getKeyNodeIndex()
                if new_id is not None:
                    self.addKeyNode(new_id, opos)
                else:
                    print("warning: can not add node!")
            elif selected:
                selected.setSelected(True)
            if isinstance(selected,EllipseItem):
                selected.setSelected(True)

        elif pos == self.__mousePressPos and (event.button() & Qt.RightButton) and self.__show_image:
            # step 1: check the mouse presse point is not exist
            isExist, selected = self.pointIsExist(pos)
            if isExist and isinstance(selected,KeyPointItem):
                self.removeKeyNode(selected)
            if isinstance(selected,EllipseItem):
                self.removeEllipseNode(selected)
        self.__mousePressPos = None  # reset mouse press pos

        QGraphicsView.mouseReleaseEvent(self, event)

    def update_ellipse(self):
        if not self.ellipse_item:
            self.ellipse_item = EllipseItem(QRectF(self.start_pos, QtCore.QSizeF()),hiden_flag =self.__hist_flag)
            if self.__hist_flag == 0:
                self.pen = QPen(QColor(255, 165, 0))
                self.ellipse_item.setPen(self.pen)
            if self.__hist_flag == 1:
                self.pen = QPen(QColor(0, 0, 255))
                self.ellipse_item.setPen(self.pen)
            if self.__hist_flag == 2:
                self.pen = QPen(QColor(0, 255, 0))
                self.ellipse_item.setPen(self.pen)

            self.scene.addItem(self.ellipse_item)
        rect = QRectF(self.start_pos, self.end_pos).normalized()
        # print("start_pos",self.start_pos)
        # print("end_pos",self.end_pos)
        self.ellipse_item.setRect(rect)

    def get_ellipse_point(self,start,end,ellipse_points_count,hist_flag,Ellipseflag_list):
        width = abs((end.x() - start.x()) / 2)
        high = abs((end.y() - start.y()) / 2)
        ellipse_center_x = (start.x() + end.x()) / 2
        ellipse_center_y = (start.y() + end.y()) / 2
        print("ellpise_center_x",ellipse_center_x)
        print("ellpise_center_y",ellipse_center_y)
        if width > high or width == high:
            long_axis = width
            short_axis = high
        else:
            long_axis = high
            short_axis = width

        for i in range(0,360,60):
            angle = math.radians(i)
            ellipse_points_count += 1
            coor_x = ellipse_center_x + long_axis * math.cos(angle)
            coor_y = ellipse_center_y + short_axis *math.sin(angle)
            self.__keyEllipseMap[ellipse_points_count]=QPoint(coor_x,coor_y)
        ellipse_points_count += 1
        for i in range(int(max_ellpise_keypoints_num/2)):
            Ellipseflag_list.append(hist_flag)
        self.__keyEllipseMap[ellipse_points_count] = QPoint(ellipse_center_x, ellipse_center_y)

    def addKeyNode(self, kid, pos, pointType=0):
        item = KeyPointItem(None, kid, self, hiden_flag=pointType)
        item.setColor(None)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(item)
        item.setPos(pos)
        self.__keyNodeMap[kid] = item
        # check and link node
        link_ids = KeyPointItem.getConnectMap_eye_10()[kid]
        for i in link_ids:
            node_is_exist = (i in self.__keyNodeMap.keys())
            if node_is_exist:
                pre_node = self.__keyNodeMap[i]
                self.addNodeEdge(pre_node, item)

    def removeKeyNode(self, node: KeyPointItem):
        # step1 remove edges
        for i in range(len(node.edges())-1, -1, -1):
            edge = node.edges()[i]
            edge.sourceNode.removeEdge(edge)
            edge.targetNode.removeEdge(edge)
            edge.prepareGeometryChange()
            self.scene.removeItem(edge)

        # step2 remove node
        node.prepareGeometryChange()
        self.scene.removeItem(node)
        for key in self.__keyNodeMap.keys():
            if self.__keyNodeMap[key] == node:
                self.__keyNodeMap.pop(key)
                break
        # print(len(self.__keyNodeMap))

    def addEllpiseNode(self, ell_id,ellipse_item):
        self.__keyEllipseMap[ell_id] = ellipse_item

    def removeEllipseNode(self,node:EllipseItem):
        node.prepareGeometryChange()
        self.scene.removeItem(node)
        for key in self.__keyEllipseMap.keys():
            if self.__keyEllipseMap[key] == node:
                self.__keyEllipseMap.pop(key)
                break
    def pointIsExist(self, pos: QPoint):
        opos = self.mapToScene(pos)
        oTrf = QTransform()
        item = self.scene.itemAt(opos, oTrf)
        if isinstance(item,EllipseItem):
            return True,item
        if item is None:
            return False, None
        elif item.flag() == 1:
            return True, item
        elif item.flag() == 0:
            return False, None
        else:
            return False, None

    def getKeyNodeIndex(self):
        for i in range(1, max_keyPoint_num + 1):
            node = self.__keyNodeMap.get(i)
            if node:
                continue
            else:
                return i

    def getEllipseNodeIndex(self):
        for i in range(1, max_ellpise_count + 1):
            node = self.__keyEllipseMap.get(i)
            if node:
                continue
            else:
                return i


    # clear all key node
    def clearAllNode(self):
        self.__keyNodeMap.clear()
        self.__keyEllipseMap.clear()
        self.scene.clear()
        self.pixItem = None
        self.scene.update()
        self.update()

    def removeSelectNode(self):
        items = self.scene.selectedItems()
        for i in range(len(items) - 1, -1, -1):
            node = items[i]
            if node.flag() == 1:
                self.removeKeyNode(node)

    def changeKeyNodeFlag(self, node: KeyPointItem, status:int):
        node.prepareGeometryChange()
        for key in self.__keyNodeMap.keys():
            if self.__keyNodeMap[key] == node:
                if status == 0:
                    self.__keyNodeMap[key].hiden_flag = 0
                elif status == 1:
                    self.__keyNodeMap[key].hiden_flag = 1
                else:
                    self.__keyNodeMap[key].hiden_flag = 2
                node.prepareGeometryChange()
                self.scene.update()

    def changeSelectNodeStatus(self, status:int):
        items = self.scene.selectedItems()
        for i in range(len(items) - 1, -1, -1):
            node = items[i]
            if node.flag() == 1:
                self.changeKeyNodeFlag(node, status)

    def hideShowNode(self, isShow):
        if self.__show_nodes and not isShow:
            # print("hide node")
            self.hideNode()
            self.scene.update()
            self.__show_nodes = False
        else:
            # print("show node")
            self.showNode()
            self.update()
            self.__show_nodes = True

    def refreshKeyNode(self, lms):
        # clear node
        # self.clearAllNode()
        # add new node
        if lms:
            lmx, lmy, pointType = lms[0], lms[1], lms[2]
            # print("refreshKeyNode lmx:%d lmy:%d" % (len(lmx), len(lmy)))
            for idx in range(max_keyPoint_num):
                x = lmx[idx]
                y = lmy[idx]
                hiden_flag = pointType[idx]
                self.addKeyNode(idx + 1, QPointF(x, y), hiden_flag)
            self.updateNodeUI()


    def through_points_draw_ellpise(self,ellpise_list):

        # 将坐标点转化为线性方程组
        x = np.array([p[0] for p in ellpise_list])
        y = np.array([p[1] for p in ellpise_list])
        A = np.vstack([x ** 2, x * y, y ** 2, x, y, np.ones(len(x))]).T
        b = np.ones(len(x))


        # 使用 polyfit 函数进行拟合
        params = np.linalg.lstsq(A, b, rcond=None)[0]
        A, B, C, D, E, F = params

        # 计算椭圆参数
        a = np.sqrt(-F / (A + C * (B / A) ** 2 - D * B / A + E * B / A))
        b = np.sqrt(-F / (A + C * (B / A) ** 2 - D * B / A + E * B / A) * A / C)
        theta = 0.5 * np.arctan2(B, A - C)

        # 计算椭圆的外接矩形
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        X = np.array([x, y])
        Q = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
        X_rot = np.dot(Q, X)
        x_min, y_min = np.min(X_rot, axis=1)
        x_max, y_max = np.max(X_rot, axis=1)
        width = x_max -x_min
        height = y_max - y_min
        rectf = QRectF(x_min,x_max,width,height)
        return rectf,x_min,x_max,y_min,y_max

    def through_points_draw_ellpise_v2(self, ellpise_list,center):
        x = np.array([p[0] for p in ellpise_list])
        y = np.array([p[1] for p in ellpise_list])
        x_new = (x - center[0]).tolist()
        y_new = (y - center[1]).tolist()
        x1,y1 =x_new[0],y_new[0]
        x2,y2 =x_new[1],y_new[1]
        x3,y3 =x_new[2],y_new[2]
        x4,y4 =x_new[3],y_new[3]
        x5,y5 =x_new[4],y_new[4]
        x6,y6 =x_new[5],y_new[5]
        if y_new[0] == 0:
            A = np.array([[1, 0], [0, 1]])
            B = np.array([y_new[0] ** 2, x_new[0] ** 2])
        # A = np.array(
        #     [[y2 ** 2 / y1 ** 2 - y3 ** 2 / y2 ** 2 + y4 ** 2 / y3 ** 2 - y5 ** 2 / y4 ** 2 + y6 ** 2 / y5 ** 2, x2 ** 2 / y1 ** 2 - x3 ** 2 / y2 ** 2 + x4 ** 2 / y3 ** 2 - x5 ** 2 / y4 ** 2 + x6 ** 2 / y5 ** 2],
        #      [y2 ** 2 / y1 ** 2 - y4 ** 2 / y3 ** 2 + y6 ** 2 / y5 ** 2,x2 ** 2 / y1 ** 2 - x4 ** 2 / y3 ** 2 + x6 ** 2 / y5 ** 2]])
    #    A = np.array(
    #        [[y2 ** 2 / y1 ** 2 - y3 ** 2 / y2 ** 2 + y4 ** 2 / y3 ** 2 - y5 ** 2 / y4 ** 2 + y6 ** 2 / y5 ** 2,x2 ** 2 / y1 ** 2 - x3 ** 2 / y2 ** 2 + x4 ** 2 / y3 ** 2 - x5 ** 2 / y4 ** 2 + x6 ** 2 / y5 ** 2],
    #         [-x2 ** 2 / y1 ** 2 + x4 ** 2 / y3 ** 2 - x6 ** 2 / y5 ** 2, x2 ** 2 / y1 ** 2 - x4 ** 2 / y3 ** 2 + x6 ** 2 / y5 ** 2]])
        else:
            A = np.array(
                [[y2 ** 2 / y1 ** 2 - y3 ** 2 / y2 ** 2 + y4 ** 2 / y3 ** 2 - y5 ** 2 / y4 ** 2 + y6 ** 2 / y5 ** 2,x2 ** 2 / y1 ** 2 - x3 ** 2 / y2 ** 2 + x4 ** 2 / y3 ** 2 - x5 ** 2 / y4 ** 2 + x6 ** 2 / y5 ** 2],
                [-x2 ** 2 / y1 ** 2 + x4 ** 2 / y3 ** 2 - x6 ** 2 / y5 ** 2,y2 ** 2 / y1 ** 2 - y4 ** 2 / y3 ** 2 + y6 ** 2 / y5 ** 2]])

            B = np.array([x1 ** 2 / y1 ** 2 - (x2 ** 2 / y1 ** 2 - y2 ** 2 / y1 ** 2),
                        y1 ** 2 / x1 ** 2 - (y2 ** 2 / x2 ** 2 - 1)])
        X = np.dot(np.linalg.inv(A), B)
        a, b = np.sqrt(X[0]), np.sqrt(X[1])
        if a > b or a == b:
            long_axis = a
            short_axis = b
            x_min = int(center[0] + long_axis)
            y_max = int(center[0] - long_axis)
            y_min = int(center[1] - short_axis)
            x_max = int(center[1] + short_axis)
            width = int(long_axis)
            height = int(short_axis)
        else:
            long_axis = b
            short_axis = a
            x_min = int(center[0] - long_axis)
            y_min = int(center[1] - short_axis)
            x_max = int(center[0] + long_axis)
            y_max = int(center[1] + short_axis)
            width = int(long_axis)
            height = int(short_axis)
        rectf = QRectF(x_min,x_max,width,height)
        return rectf,x_min,x_max,y_min,y_max
    def hideNode(self):
        for key in list(self.__keyNodeMap):
            node = self.__keyNodeMap.get(key)
            # hide edges
            for i in range(len(node.edges()) - 1, -1, -1):
                edge = node.edges()[i]
                edge.hide()
            node.hide()

    def showNode(self):
        for key in list(self.__keyNodeMap):
            node = self.__keyNodeMap.get(key)
            # show edges
            for i in range(len(node.edges()) - 1, -1, -1):
                edge = node.edges()[i]
                edge.show()
            node.show()

    def addNodeEdge(self, pre, next):
        if pre and next:
            edge = KeyEdgeItem(None, pre, next, self)
            self.scene.addItem(edge)

    def collectFeatureData(self):
        nodes = self.__keyNodeMap
        img_data = dataset.ImageFeatureData()
        data = dataset.FeatureData()

        for key in sorted(self.__keyNodeMap.keys()):
            node = self.__keyNodeMap[key]
            pos = node.pos()
            x = pos.x()
            y = pos.y()
            is_hiden = node.hiden_flag

            # print("key: ", key, " ", pos)
            data.lmx.append(x)
            data.lmy.append(y)
            data.is_hiden.append(is_hiden)


        for ellpise_key in sorted(self.__keyEllipseMap.keys()):
            node = self.__keyEllipseMap[ellpise_key]
            is_hiden = node.hiden_flag
            rect = node.boundingRect()
            w = rect.width()
            h = rect.height()
            width = w / 2
            height = h / 2
            ellipse_center_x = rect.center().x()
            ellipse_center_y = rect.center().y()

            if width > height or width == height:
                long_axis = width
                short_axis = height

            else:
                long_axis = height
                short_axis = width
            for i in range(0, 360, 90):
                angle = math.radians(i)
                # coor_x = int(ellipse_center_x + short_axis * math.cos(angle))
                # coor_y = int(ellipse_center_y + long_axis * math.sin(angle))
                coor_x = int(ellipse_center_x + width * math.cos(angle))
                coor_y = int(ellipse_center_y + height * math.sin(angle))
                data.lmx.append(coor_x)
                data.lmy.append(coor_y)
                data.is_hiden.append(is_hiden)
            data.lmx.append(int(ellipse_center_x))
            data.lmy.append(int(ellipse_center_y))
            data.is_hiden.append(is_hiden)

        img_data.features.append(data)
        img_data.img_info = self.__show_image
        self.__hist_flag = 0
        return img_data

    def setScaleFactor(self, factor):
        if factor == self.scale_factor:
            return
        if (factor >= 0.1) and (factor <= 10.0):
            # First, go back to the base scale  (1.0 or 100%)
            adjust = 1.0 / self.scale_factor
            print("adjust ", adjust)
            self.scale(adjust, adjust)
            # Then, apply the requested factor.
            self.scale_factor = factor
            print("new scale: ", self.scale_factor)
            if self.scale_factor != 1.0:
                self.scale(self.scale_factor, self.scale_factor)

    def scaleViewBy(self, factor):
        dFactor = self.scale_factor * factor
        if (dFactor >= 0.1) and (dFactor <= 10.0):
            self.scale_factor = dFactor

            self.font_size = FONT_SIZE / self.scale_factor
            if self.font_size > FONT_SIZE:
                self.font_size = FONT_SIZE
            elif self.font_size < 1:
                self.font_size = 1
            font = self.font()
            font.setPixelSize(int(self.font_size))
            self.setFont(font)


            # print("scaleViewBy ", self.scale_factor)
            self.scale(factor, factor)
            # emit the signal that the scale factor has changed
            self.onScaleFactorChanged.emit(self.getScaleFactor())
            # update ui
            self.updateNodeUI()

    def zoomReset(self):
        self.scale_factor = 1.0
        self.scaleViewBy(1.0)

    def zoomIn(self):
        self.scaleViewBy(ZOOM_IN_STEP)

    def zooOut(self):
        self.scaleViewBy(ZOOM_OUT_STEP)

    def getScaleFactor(self):
        # print("getScaleFactor scale_factor:", self.scale_factor)
        return math.floor(self.scale_factor * 100000.0) / 100000.0

    def wheelEvent(self, event: QWheelEvent):
        b_ctrl = QApplication.keyboardModifiers() & Qt.ControlModifier
        b_Alt = QApplication.keyboardModifiers() & Qt.AltModifier
        b_Shift = QApplication.keyboardModifiers() & Qt.ShiftModifier
        delta = event.angleDelta().x() + event.angleDelta().y()
        base = ZOOM_IN_STEP
        if delta < 0:
            base = ZOOM_OUT_STEP
        step = math.fabs(delta / 120)
        if not (b_ctrl or b_Alt or b_Shift):
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta)
        elif b_Shift and not (b_ctrl or b_Alt):
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta)
        elif b_ctrl and not (b_Alt or b_Shift):
            self.scaleViewBy(math.pow(base, step))

    def setDisplayFeaturesIds(self, state):
        self.__display_ids = state
        self.updateNodeUI()

    def displayFeatureIds(self):
        return self.__display_ids

    def updateNodeUI(self):
        for key in self.__keyNodeMap.keys():
            node = self.__keyNodeMap[key]
            node.prepareGeometryChange()
            node.update()
            node.updateEdge()
        self.update()

    def setNodeColor(self, color):
        self.__node_color = color
        for item in self.scene.selectedItems():
            if item.flag() == 1:
                item.setColor(self.__node_color)


