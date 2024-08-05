#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : KeyPointItem.py

from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPolygon

from EdgeItem import KeyEdgeItem

RADIUS = 1


class KeyPointItem(QGraphicsItem):
    def __init__(self, parent=None, key=0, widget: QGraphicsView = None, hiden_flag = 0):
        QGraphicsItem.__init__(self, parent)
        self.pWidget = widget
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        # self.setSelected(True)
        self.setAcceptDrops(True)
        self.hiden_flag = hiden_flag
        # self.setAcceptedMouseButtons(Qt.NoButton)
        self.__id = key
        self.__flag = 1
        self.__m_lEdges = []
        self.__color = QColor(255, 255, 0)
        self.__color_hiden = QColor(255, 255, 153)
        self.__color_miss = QColor(51, 102, 204)
    def id(self):
        return self.__id

    def setColor(self, color):
        if color is None:
            cid = KeyPointItem.getDefaultGroupMap_eye_16()[self.__id]
            c = KeyPointItem.getDefaultColorMap()[cid]
            self.__color.setRgb(c[0], c[1], c[2])
        elif color != self.__color:
            self.__color = color
            self.update()


    def boundingRect(self):
        radius = RADIUS
        radius = int(self.pWidget.font().pixelSize() / 2)
        if radius <= 0:
            radius = 1
        if self.pWidget.displayFeatureIds():
            sid = str(self.__id)
            iheight = self.pWidget.fontMetrics().height()
            iwidth = self.pWidget.fontMetrics().width(sid)
            return QRectF(-(iwidth + radius), -(iheight + radius), 2 * radius + iwidth, 2 * radius + iheight)
        else:
            return QRectF(-radius, -radius, 2 * radius, 2 * radius)

    def paint(self, painter: QPainter, option, widget):
        if self.hiden_flag == 1:
            colors = self.__color_hiden
        elif self.hiden_flag == 2:
            colors = self.__color_miss
        else:
            colors = self.__color
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        if self.isSelected():
            painter.setPen(QPen(Qt.red, 0))
            brush.setColor(QColor(Qt.red))
        else:
            painter.setPen(QPen(colors, 0))
            brush.setColor(QColor(colors))

        radius = RADIUS
        radius = int(self.pWidget.font().pixelSize() / 2)
        if radius <= 0:
            radius = 1
        if self.pWidget.displayFeatureIds():
            sid = str(self.__id)
            iheight = self.pWidget.fontMetrics().height()
            iwidth = self.pWidget.fontMetrics().width(sid)
            # print("item paint text (%d, %d)" % (iwidth, iheight))
            rect = QRectF(-(iwidth + radius), -(iheight + radius), iwidth, iheight)
            painter.drawText(rect, sid)
            rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)
        else:
            # rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)
            rect = self.boundingRect()
        painter.setBrush(brush)
        if self.hiden_flag == 1:
            painter.drawRect(rect)
        elif self.hiden_flag == 2:
            points = QPolygon([
                QPoint(0,0),
                QPoint(-radius,2*radius),
                QPoint(radius,2*radius),
                QPoint(0,0),
            ])
            points.translate(QPoint(0, -radius))
            painter.drawPolygon(points)

            # painter.drawRoundedRect(rect, 50, 50, Qt.RelativeSize)
        else:
            painter.drawEllipse(rect)

    def flag(self):
        return self.__flag

    def addEdge(self, edge: KeyEdgeItem):
        self.__m_lEdges.append(edge)
        edge.adjust()

    def removeEdge(self, edge: KeyEdgeItem):
        self.__m_lEdges.remove(edge)

    def edges(self):
        return self.__m_lEdges

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, Any):
        if change == QGraphicsItem.ItemPositionChange:
            for edge in list(self.__m_lEdges):
                edge.adjust()
        else:
            pass
        return QGraphicsItem.itemChange(self, change, Any)

    def updateEdge(self):
        for edge in self.__m_lEdges:
            edge.prepareGeometryChange()
            edge.adjust()
            edge.update()
    # 106 landmark point
    @staticmethod
    def getConnectMap2():
        node_connect_map = {
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6],
            6: [5, 7],
            7: [6, 8],
            8: [7, 9],
            9: [8, 10],
            10: [9, 11],
            11: [10, 12],
            12: [11, 13],
            13: [12, 14],
            14: [13, 15],
            15: [14, 16],
            16: [15, 17],
            17: [16, 18],
            18: [17, 19],
            19: [18, 20],
            20: [19, 21],
            21: [20, 22],
            22: [21, 23],
            23: [22, 24],
            24: [23, 25],
            25: [24, 26],
            26: [25, 27],
            27: [26, 28],
            28: [27, 29],
            29: [28, 30],
            30: [29, 31],
            31: [30, 32],
            32: [31, 33],
            33: [32],
            # left eyebrow
            34: [35, 42],
            35: [34, 36],
            36: [35, 37],
            37: [36, 38],
            38: [37, 39],
            39: [38, 40],
            40: [39, 41],
            41: [40, 42],
            42: [41, 34],
            # right eyebrow
            43: [44, 51],
            44: [43, 45],
            45: [44, 46],
            46: [45, 47],
            47: [46, 48],
            48: [47, 49],
            49: [48, 50],
            50: [49, 51],
            51: [43, 50],
            # nose
            52: [53],
            53: [52, 54],
            54: [53, 55, 57, 65],
            55: [54],
            56: [66],
            57: [54, 58],
            58: [57, 59],
            59: [58, 60],
            60: [59, 61],
            61: [60, 62],
            62: [61, 63],
            63: [62, 64],
            64: [63, 65],
            65: [64, 54],

            66: [56],
            # left eye
            67: [68, 74],
            68: [67, 69],
            69: [68, 70],
            70: [69, 71],
            71: [70, 72],
            72: [71, 73],
            73: [72, 74],
            74: [67, 73],
            75: [],
            # right eye
            76: [77, 83],
            77: [76, 78],
            78: [77, 79],
            79: [78, 80],
            80: [79, 81],
            81: [80, 82],
            82: [81, 83],
            83: [82, 76],
            84: [],
            # mouth
            85: [86, 96],
            86: [85, 87],
            87: [86, 88],
            88: [87, 89],
            89: [88, 90],
            90: [89, 91],
            91: [90, 92],
            92: [91, 93],
            93: [92, 94],
            94: [93, 95],
            95: [94, 96],
            96: [95, 85],

            97: [98, 104],
            98: [97, 99],
            99: [98, 100],
            100: [99, 101],
            101: [100, 102],
            102: [101, 103],
            103: [102, 104],
            104: [103, 97],

            105: [],
            106: []
        }
        return node_connect_map

    @staticmethod
    def getConnectMap():
        node_connect_map = {
            1: [2],
            2: [1, 3],
            3: [2],
            # left eyebrow
            4: [5],
            5: [4, 6],
            6: [5],
            # right eyebrow
            7: [8],
            8: [7, 9],
            9: [8, 10],
            10: [9, 11],
            11: [10],
            # left eye
            12: [13],
            13: [12, 14],
            14: [13, 15],
            15: [14, 16],
            16: [15],
            # right eye
            17: [18],
            18: [17, 19],
            19: [18, 20],
            20: [19],
            # nose
            21: [22],
            22: [21, 23],
            23: [22, 24],
            24: [23, 25],
            25: [24, 26],
            26: [25, 27],
            27: [26],
            # mouth
        }
        return node_connect_map
    # 28 eye keypoints
    @staticmethod
    def getConnectMap_eye_28():
        node_connect_map = {
            #left eyelids
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6],
            6: [5, 7],
            7: [6, 8],
            8: [1, 7],
            # left iris
            9: [10],
            10: [9, 11],
            11: [10, 12],
            12: [11, 13],
            13: [9, 12],
            #left pupil
            14: [],
            #right eyelids
            15: [16],
            16: [15, 17],
            17: [16, 18],
            18: [17, 19],
            19: [18, 20],
            20: [19, 21],
            21: [20, 22],
            22: [15, 21],
            #right iris
            23: [24],
            24: [23, 25],
            25: [24, 26],
            26: [25, 27],
            27: [23, 26],
            #right pupil
            28: []
        }
        return node_connect_map

    @staticmethod
    def getConnectMap_eye_16():
        node_connect_map = {
            #left eyelids
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 6],
            6: [5, 7],
            7: [6, 8],
            8: [1, 7],
            #right eyelids
            9: [10],
            10: [9, 11],
            11: [10, 12],
            12: [11, 13],
            13: [12, 14],
            14: [13, 15],
            15: [14, 16],
            16: [15, 9],
        }
        return node_connect_map

    @staticmethod
    def getConnectMap_eye_10():
        node_connect_map = {
            #left eyelids
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4],
            #right eyelids
            6: [7],
            7: [6, 8],
            8: [7, 9],
            9: [8,10],
            10: [9]
        }
        return node_connect_map
    @staticmethod
    def getDefaultColorMap():
        node_default_color_map = {
            0: [102, 51, 0],
            1: [0, 102, 0],
            2: [255, 102, 204],
            3: [153, 102, 255],
            4: [255, 102, 0],
            5: [102, 204, 255],
            6: [255, 255, 153],
            7: [51, 102, 204]
        }
        return node_default_color_map
    # 106 landmark point
    @staticmethod
    def getDefaultGroupMap222():
        node_default_group_map = {
            #
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0,
            25: 0,
            26: 0,
            27: 0,
            28: 0,
            29: 0,
            30: 0,
            31: 0,
            32: 0,
            33: 0,
            # left eyebrow
            34: 1,
            35: 1,
            36: 1,
            37: 1,
            38: 1,
            39: 1,
            40: 1,
            41: 1,
            42: 1,
            # right eyebrow
            43: 2,
            44: 2,
            45: 2,
            46: 2,
            47: 2,
            48: 2,
            49: 2,
            50: 2,
            51: 2,
            # nose
            52: 3,
            53: 3,
            54: 3,
            55: 3,
            56: 3,
            57: 3,
            58: 3,
            59: 3,
            60: 3,
            61: 3,
            62: 3,
            63: 3,
            64: 3,
            65: 3,
            66: 3,

            # left eye
            67: 4,
            68: 4,
            69: 4,
            70: 4,
            71: 4,
            72: 4,
            73: 4,
            74: 4,
            75: 4,
            # right eye
            76: 5,
            77: 5,
            78: 5,
            79: 5,
            80: 5,
            81: 5,
            82: 5,
            83: 5,
            84: 5,
            # mouth
            85: 6,
            86: 6,
            87: 6,
            88: 6,
            89: 6,
            90: 6,
            91: 6,
            92: 6,
            93: 6,
            94: 6,
            95: 6,
            96: 6,

            97: 6,
            98: 6,
            99: 6,
            100: 6,
            101: 6,
            102: 6,
            103: 6,
            104: 6,

            105: 7,
            106: 7
        }
        return node_default_group_map

    # 28 eye keypoints
    @staticmethod
    def getDefaultGroupMap_eye_28():
        node_default_group_map = {
            #left eyelids
            1: 2,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            #left iris
            9: 4,
            10: 4,
            11: 4,
            12: 4,
            13: 4,
            #left pupil
            14: 5,
            #right eyelibs
            15: 2,
            16: 2,
            17: 2,
            18: 2,
            19: 2,
            20: 2,
            21: 2,
            22: 2,
            #right iris
            23: 4,
            24: 4,
            25: 4,
            26: 4,
            27: 4,
            #right pupil
            28: 5,
        }
        return node_default_group_map

    @staticmethod
    def getDefaultGroupMap_eye_16():
        node_default_group_map = {
            #left eyelids
            1: 2,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            #right eyelibs
            9: 2,
            10: 2,
            11: 2,
            12: 2,
            13: 2,
            14: 2,
            15: 2,
            16: 2,
        }
        return node_default_group_map

    @staticmethod
    def getDefaultGroupMap():
        node_default_group_map = {
            1: 0,
            2: 0,
            3: 0,
            # left eyebrow
            4: 1,
            5: 1,
            6: 1,
            # right eyebrow
            7: 2,
            8: 2,
            9: 2,
            10: 2,
            11: 2,
            # left eye
            12: 3,
            13: 3,
            14: 3,
            15: 3,
            16: 3,
            # right eye
            17: 4,
            18: 4,
            19: 4,
            20: 4,
            # nose
            21: 5,
            22: 5,
            23: 5,
            24: 5,
            25: 5,
            26: 5,
            27: 5,
            # mouth
        }
        return node_default_group_map
