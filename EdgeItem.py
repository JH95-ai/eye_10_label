#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : EdgeItem.py

from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF, QSizeF, QLineF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor

import KeyPointItem


class KeyEdgeItem(QGraphicsItem):
    def __init__(self, parent=None, source: KeyPointItem=None, target: KeyPointItem = None, widget: QGraphicsView = None):
        QGraphicsItem.__init__(self, parent)
        # private variable
        self.pWidget = widget
        self.__flag = 2
        self.prepareGeometryChange()
        self.sourceNode = source
        self.targetNode = target
        self.sourceNode.addEdge(self)
        self.targetNode.addEdge(self)
        self.m_oSourceNode = self.sourceNode.pos()
        self.m_oTargetNode = self.targetNode.pos()
        self.adjust()

    def boundingRect(self):
        # if self.sourceNode and self.targetNode:
        #     rect = QRectF(self.sourceNode.pos(), QSizeF(self.targetNode.x() - self.sourceNode.x(),
        #                                                 self.targetNode.y() - self.sourceNode.y()))
        #     return rect
        # else:
        #     return QRectF()
        if self.sourceNode and self.targetNode:
            rect = QRectF(self.m_oSourceNode, QSizeF(self.m_oTargetNode.x() - self.m_oSourceNode.x(),
                                                     self.m_oTargetNode.y() - self.m_oSourceNode.y()))
            return rect.normalized()
        else:
            return QRectF()

    def flag(self):
        return self.__flag

    def paint(self, painter: QPainter, option, widget):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(QPen(Qt.green, 0))
        brush.setColor(QColor(Qt.green))
        painter.setBrush(brush)
        painter.drawLine(self.m_oSourceNode, self.m_oTargetNode)

    def adjust(self):
        line = QLineF(self.mapFromItem(self.sourceNode, 0, 0), self.mapFromItem(self.targetNode, 0, 0))
        length = line.length()
        self.prepareGeometryChange()
        self.m_oSourceNode = line.p1()
        self.m_oTargetNode = line.p2()
        radius = KeyPointItem.RADIUS
        radius = int(self.pWidget.font().pixelSize() / 2)
        if radius <= 0:
            radius = 1
        # print("adjust radius%d lengthL:%d" % (radius, length))
        if length <= 0:
            edge_offset = QPointF(0.0, 0.0)
        else:
            edge_offset = QPointF(line.dx() * radius / length, line.dy() * radius / length)
        self.m_oSourceNode = line.p1() + edge_offset
        self.m_oTargetNode = line.p2() - edge_offset
