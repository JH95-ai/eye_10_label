from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, \
    QGraphicsSceneDragDropEvent, QGraphicsSceneMouseEvent, QApplication,QGraphicsEllipseItem
class EllipseItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, rect,hiden_flag):
        super().__init__(rect)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemIsSelectable | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.__flag = 0
        self.hiden_flag = hiden_flag
        self.move_start_press = None
        self.move_end_press = None
    def flag(self):
        return self.__flag

    def set_ellipse_rect(self, rect):
        # 自定义逻辑
        self.setRect(rect)
    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     if event.button() == Qt.LeftButton:
    #         # 记录鼠标按下时的位置和图形项的偏移量
    #         self.move_start_press = self.move_end_press = self.mapToScene(event.pos())

    # def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     if event.buttons() == Qt.LeftButton:
    #         self.move_end_press = self.mapToScene(event.pos())
    #         # 计算鼠标移动的距离，并更新图形项的位置属性
    #         # self.setPos(self.move_end_press - self.move_start_press)

    # def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     if event.button() == Qt.LeftButton:
    #         self.move_end_press = self.mapToScene(event.pos())
    #         self.setPos(self.move_end_press - self.move_start_press)
    #         # print("changed_setpos",self.move_end_press)

    # def itemChange(self, change: QGraphicsItem.GraphicsItemChange, Any):
    #     # if change == QGraphicsItem.ItemPositionChange:
    #     #     # 当位置改变时，调整椭圆的起始角度，使其始终面向鼠标
    #     #     new_pos = Any.toPoint()
    #     #     cursor_pos = self.scene().views()[0].mapFromGlobal(QCursor.pos())
    #     #     dx = cursor_pos.x() - new_pos.x()
    #     #     dy = cursor_pos.y() - new_pos.y()
    #     #     # angle = 0 if dx == 0 else abs(dy / dx)
    #     #     # if dx < 0 and dy < 0:
    #     #     #     angle = 180 - angle
    #     #     # elif dx < 0 and dy > 0:
    #     #     #     angle = 180 + angle
    #     #     # elif dx > 0 and dy > 0:
    #     #     #     angle = 360 - angle
    #     #     # self.setStartAngle(int(angle * 16))
    #     # else:
    #     #     pass
    #     # return super().itemChange(change, Any)
    #     pass
