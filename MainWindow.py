
import os

from PyQt5.QtWidgets import QMainWindow, QWidget


from MainWindow_ui import Ui_MainWindow

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QFileDialog, QToolTip, QColorDialog, QMessageBox
from PyQt5.QtGui import QKeyEvent
import PyQt5.QtWidgets
import PyQt5.QtCore

from image_widget import ImageWidget

import tools.file as file_tool
test_img = '/home/ts-liqing/iwork/project/Face/Tool/Facial-Landmarks-Annotation-Tool/example/images/Angelina.jpg'


class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # varible
        self.source_directory = None
        self.img_list = []
        self.tagging_list = []
        self.index = 0
        self.currentShowImg = test_img
        self.save_directory = ''
        self.tagging_list_file = ''

        # add widget to tab widget
        self.widget = ImageWidget(self.tabWidget)
        self.tabWidget.addTab(self.widget, 'tab')
        self.widget.installEventFilter(self)

        # connect
        self.widget.onUIUpdated.connect(self.onChildZoomUpdated)
        self.start = None
        self.end = None
    def showImage(self, file):
        self.widget.removeAllFeatures()
        self.widget.updateImage(file)
        # self.preload_chbox.setChecked(False)

    def on_loadbtn_pressed_slot(self):
        print("on_loadbtn_pressed")
        self.source_directory = QFileDialog.getExistingDirectory()
        if self.source_directory:
            self.source_path_show.setText(self.source_directory)
            self.img_list = file_tool.eachFiles(self.source_directory)
            # read do tagging list file
            self.tagging_list_file = os.path.join(self.source_directory, 'doTaggingList.json')
            if os.path.exists(self.tagging_list_file):
                self.tagging_list = file_tool.readDoTaggingFile(self.tagging_list_file)
            else:
                self.tagging_list = file_tool.createDoTaggingList(self.img_list)
            img_count = len(self.tagging_list)
            self.index = 0
            print("Info: There are", img_count, " images.")
            self.nextImage()
            print("The current show image index:", self.index)
            if img_count > 0:
                self.currentShowImg = os.path.join(self.source_directory, self.tagging_list[self.index].img)
                print("The image name is: ",self.currentShowImg)
                self.showImage(self.currentShowImg)
            else:
                print("Warning: current diectory has no image.")
        else:
            print("cancel file dialog!")

    def nextImage(self):
        for index, item in enumerate(self.tagging_list):
            if item.img != '' and item.tagging_file == '':
                self.index = index
                break
            else:
                continue

    def setTaggingFile(self, tag_file):
        for index, item in enumerate(self.tagging_list):
            if item.img == self.currentShowImg:
                item.tagging_file = tag_file
                break
            else:
                continue

    def on_choose_save_btn_pressed_slot(self):
        print("on_choose_save_btn_pressed_slot")
        self.save_directory = QFileDialog.getExistingDirectory()
        if self.save_directory:
            self.save_path_show.setText(self.save_directory)
        else:
            print("cancel file dialog!")

    def on_next_btn_pressed_slot(self):
        print("on_after_btn_pressed_slot")
        if self.save_directory and self.save_directory != '':
            # update tagging list
            _name = os.path.basename(self.currentShowImg)
            tagging_out_file = os.path.join(self.save_directory, _name.split('.')[0] + ".json")
            self.setTaggingFile(tagging_out_file)
            out_file = os.path.join(self.source_directory, 'doTaggingList.json')
            print("do tagging file: ", out_file)
            file_tool.writeDoTaggingFile(out_file, self.tagging_list)

            self.widget.saveResult(self.save_directory)
            QToolTip.showText(QPoint(700, 700), "save finish!")
        else:
            button = QMessageBox.warning(self, "Warning", "Fail, can't found save directory!",
                                         QMessageBox.Ok)
            print("Error: The output directory is none!")

        if self.tagging_list and len(self.tagging_list) > 0:
            if self.index < len(self.tagging_list) - 1:
                self.index = self.index + 1
                print("The next image index:", self.index)
                self.currentShowImg = os.path.join(self.source_directory, self.tagging_list[self.index].img)
                print("The image name is: ", self.currentShowImg)
                # show image
                item = self.tagging_list[self.index]
                # img = self.img_list[self.index]
                self.currentShowImg = os.path.join(self.source_directory, item.img)
                self.showImage(self.currentShowImg)
                # read and show tagging data
                self.widget.updateTaggingData(item.tagging_file)
                QToolTip.showText(QPoint(700, 700), "next finish!")
                print("next finish!!!")
            else:
                print("This is the last image.")
        else:
            print("Warning: Please load image path first!")

    def on_preivous_btn_pressed_slot(self):
        print("on_preivous_btn_pressed_slot")
        if self.tagging_list and len(self.tagging_list) > 0:
            if self.index > 0:
                self.index = self.index - 1
                print("The previous image index:", self.index)
                # show iamge
                item = self.tagging_list[self.index]
                # img = self.img_list[self.index]
                self.currentShowImg = os.path.join(self.source_directory, item.img)
                self.showImage(self.currentShowImg)
                # read and show tagging data
                self.widget.updateTaggingData(item.tagging_file)
                QToolTip.showText(QPoint(700, 700), "previous!")
            else:
                print("This is the first image.")
        else:
            print("Warning: Please load image path first!")

    def on_save_btn_pressed_slot(self):
        print("on_save_btn_pressed_slot")
        if self.save_directory and self.save_directory != '':
            # update tagging list
            _name = os.path.basename(self.currentShowImg)
            tagging_out_file = os.path.join(self.save_directory, _name.split('.')[0] + ".json")
            self.setTaggingFile(tagging_out_file)
            out_file = os.path.join(self.source_directory, 'doTaggingList.json')
            print("do tagging file: ", out_file)
            file_tool.writeDoTaggingFile(out_file, self.tagging_list)

            self.widget.saveResult(self.save_directory)
            QToolTip.showText(QPoint(700, 700), "save finish!")
        else:
            button = QMessageBox.warning(self, "Warning", "Fail, can't found save directory!",
                                         QMessageBox.Ok)
            print("Error: The output directory is none!")

    def on_delete_btn_pressed_slot(self):
        print("on_delete_btn_pressed_slot")
        self.widget.removeSelectFeatures()
        QToolTip.showText(QPoint(700, 700), "delete finish!")


    def mousePressEvent(self, e):
        pass

    # def paintEvent(self, e):
    #     painter = PyQt5.QtGui.QPainter(self)
    #     pen = PyQt5.QtGui.QPen(Qt.red, 3)
    #     painter.setPen(pen)
    #
    #     if self.start and self.end:
    #         center = QPoint((self.start.x() + self.end.x()) / 2,
    #                          (self.start.y() + self.end.y()) / 2)
    #         rx = abs((self.end.x() - self.start.x()) / 2)
    #         ry = abs((self.end.y() - self.start.y()) / 2)
    #         painter.drawEllipse(center, rx, ry)
    #
    # def mousePressEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.start = e.pos()
    #
    # def mouseMoveEvent(self, e):
    #     if e.buttons() == Qt.LeftButton:
    #         self.end = e.pos()
    #         self.update()
    #
    # def mouseReleaseEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.end = e.pos()
    #         self.update()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_A:  # A -> befroe
            print("keyPressEvent A -> Previous")
            self.on_preivous_btn_pressed_slot()
        elif e.key() == Qt.Key_S:  # S -> Save
            print("keyPressEvent S -> Save")
            self.on_save_btn_pressed_slot()
        elif e.key() == Qt.Key_D:   # D -> Delete
            print("keyPressEvent D -> Delete")
            self.on_delete_btn_pressed_slot()
        elif e.key() == Qt.Key_E:   # E -> Normal flag
            print("keyPressEvent E -> Normal_btn")
            self.on_normal_btn_pressed_slot()
        elif e.key() == Qt.Key_F:   # F -> Next
            print("keyPressEvent F -> Next")
            self.on_next_btn_pressed_slot()
        elif e.key() == Qt.Key_R:   # R -> Hiden flag
            print("keyPressEvent R -> Occlusion_btn")
            self.on_hiden_btn_pressed_slot()
        elif e.key() == Qt.Key_T:   # T -> Miss flag
            print("keyPressEvent T -> Self-Occlusion_btn")
            self.on_miss_btn_pressed_slot()
        elif e.key() == Qt.Key_I:
            print("keyPressEvent I -> draw_oval")
            self.on_draw_oval_pressed_slot()
        elif e.key() == Qt.Key_O:
            print("keyPressEvent O -> draw_occlusion_oval")
            self.on_draw_occlusion_oval_pressed_slot()
        elif e.key() == Qt.Key_P:
            print("keyPressEvent P -> draw_self_occlusion_oval")
            self.on_draw_self_occlusion_oval_pressed_slot()


        elif e.key() == Qt.Key_Plus:  # ctrl +
            self.widget.zoomIn()
            e.accept()
        elif e.key() == Qt.Key_Minus:
            self.widget.zoomOut()
            e.accept()
        else:
            QMainWindow.keyPressEvent(self, e)

    def on_zoomSlider_valueChanged_slot(self, value):
        print("value ", value)
        self.zoomSlider.blockSignals(True)
        self.zoomSlideValue = self.zoomSlider.value()
        self.widget.setZoomLevel(self.zoomSlideValue)
        self.zoomSlider.blockSignals(False)
        print("zoom slider value is ", self.zoomSlideValue)

    def onChildZoomUpdated(self, zoomLevel):
        # Zoom level
        self.zoomSlider.blockSignals(True)
        self.zoomSlider.setValue(zoomLevel)
        self.zoomSlider.blockSignals(False)

    def on_show_ids_stateChanged_slot(self, state):
        pass
        if state == Qt.Unchecked:
            self.widget.setDisplayFeaturesIds(False)
        else:
            self.widget.setDisplayFeaturesIds(True)

    def on_color_btn_pressed_slot(self):
        color = QColorDialog.getColor()
        if color:
            self.widget.setFeatureColor(color)
            style = "QPushButton {background-color: rgb(" + str(color.red()) + "," + str(color.green()) + "," \
                    + str(color.blue()) + ");}"
            self.color_btn.setStyleSheet(style)

    def on_hiden_btn_pressed_slot(self):
        self.widget.changeInSelectFeaturesToHiden()
        QToolTip.showText(QPoint(700, 700), "Occlusion point!")


    def on_miss_btn_pressed_slot(self):
        self.widget.changeInSelectFeaturesToMiss()
        QToolTip.showText(QPoint(700, 700), "Self-Occlusion point!")

    def on_normal_btn_pressed_slot(self):
        self.widget.changeInSelectFeaturesToNormal()
        QToolTip.showText(QPoint(700, 700), "Normal point!")
