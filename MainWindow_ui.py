# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def __init__(self, parent=None):
        self.tabWidget = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 800)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 736, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(539, 172))
        self.dockWidget.setObjectName("dockWidget")
        self.content = QtWidgets.QWidget()
        self.content.setObjectName("content")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.content)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.source_path = QtWidgets.QLabel(self.content)
        self.source_path.setObjectName("source_path")
        self.horizontalLayout_2.addWidget(self.source_path)
        self.source_path_show = QtWidgets.QLabel(self.content)
        self.source_path_show.setText("")
        self.source_path_show.setObjectName("source_path_show")
        self.horizontalLayout_2.addWidget(self.source_path_show)
        self.loadbtn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadbtn.sizePolicy().hasHeightForWidth())
        self.loadbtn.setSizePolicy(sizePolicy)
        self.loadbtn.setObjectName("loadbtn")
        self.loadbtn.pressed.connect(self.on_loadbtn_pressed_slot)
        self.horizontalLayout_2.addWidget(self.loadbtn)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 10)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.save_path = QtWidgets.QLabel(self.content)
        self.save_path.setObjectName("save_path")
        self.horizontalLayout_4.addWidget(self.save_path)
        self.save_path_show = QtWidgets.QLabel(self.content)
        self.save_path_show.setText("")
        self.save_path_show.setObjectName("save_path_show")
        self.horizontalLayout_4.addWidget(self.save_path_show)
        self.choose_save_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_save_btn.sizePolicy().hasHeightForWidth())
        self.choose_save_btn.setSizePolicy(sizePolicy)
        self.choose_save_btn.setObjectName("choose_save_btn")
        self.choose_save_btn.pressed.connect(self.on_choose_save_btn_pressed_slot)
        self.horizontalLayout_4.addWidget(self.choose_save_btn)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 10)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.preivous_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preivous_btn.sizePolicy().hasHeightForWidth())
        self.preivous_btn.setSizePolicy(sizePolicy)
        self.preivous_btn.setObjectName("preivous_btn")
        self.preivous_btn.pressed.connect(self.on_preivous_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.preivous_btn)

        self.next_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_btn.sizePolicy().hasHeightForWidth())
        self.next_btn.setSizePolicy(sizePolicy)
        self.next_btn.setObjectName("next_btn")
        self.next_btn.pressed.connect(self.on_next_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.next_btn)

        self.save_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setObjectName("save_btn")
        self.save_btn.pressed.connect(self.on_save_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.save_btn)

        self.normal_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normal_btn.sizePolicy().hasHeightForWidth())
        self.normal_btn.setSizePolicy(sizePolicy)
        self.normal_btn.setObjectName("normal_btn")
        self.normal_btn.pressed.connect(self.on_normal_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.normal_btn)

        self.hiden_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hiden_btn.sizePolicy().hasHeightForWidth())
        self.hiden_btn.setSizePolicy(sizePolicy)
        self.hiden_btn.setObjectName("occlusion_btn")
        self.hiden_btn.pressed.connect(self.on_hiden_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.hiden_btn)

        self.miss_btn = QtWidgets.QPushButton(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.miss_btn.sizePolicy().hasHeightForWidth())
        self.miss_btn.setSizePolicy(sizePolicy)
        self.miss_btn.setObjectName("self-occlusion_btn")
        self.miss_btn.pressed.connect(self.on_miss_btn_pressed_slot)
        self.horizontalLayout_3.addWidget(self.miss_btn)

        # self.delete_btn = QtWidgets.QPushButton(self.content)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        # self.delete_btn.setSizePolicy(sizePolicy)
        # self.delete_btn.setObjectName("delete_btn")
        # self.delete_btn.pressed.connect(self.on_delete_btn_pressed_slot)

        # self.draw_oval_btn = QtWidgets.QPushButton(self.content)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.draw_oval_btn.sizePolicy().hasHeightForWidth())
        # self.draw_oval_btn.setSizePolicy(sizePolicy)
        # self.draw_oval_btn.setObjectName("oval")
        # self.draw_oval_btn.pressed.connect(self.on_draw_oval_pressed_slot)
        # self.horizontalLayout_3.addWidget(self.draw_oval_btn)

        # self.draw_occlusion_oval_btn = QtWidgets.QPushButton(self.content)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.draw_occlusion_oval_btn.sizePolicy().hasHeightForWidth())
        # self.draw_occlusion_oval_btn.setSizePolicy(sizePolicy)
        # self.draw_occlusion_oval_btn.setObjectName("occlusion_oval")
        # self.draw_occlusion_oval_btn.pressed.connect(self.on_draw_occlusion_oval_pressed_slot)
        # self.horizontalLayout_3.addWidget(self.draw_occlusion_oval_btn)

        # self.draw_self_occlusion_oval_btn = QtWidgets.QPushButton(self.content)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.draw_self_occlusion_oval_btn.sizePolicy().hasHeightForWidth())
        # self.draw_self_occlusion_oval_btn.setSizePolicy(sizePolicy)
        # self.draw_self_occlusion_oval_btn.setObjectName("self_occlusion_oval")
        # self.draw_self_occlusion_oval_btn.pressed.connect(self.on_draw_self_occlusion_oval_pressed_slot)
        # self.horizontalLayout_3.addWidget(self.draw_self_occlusion_oval_btn)

        # self.preload_chbox = QtWidgets.QCheckBox(self.content)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.preload_chbox.sizePolicy().hasHeightForWidth())
        # self.preload_chbox.setSizePolicy(sizePolicy)
        # self.preload_chbox.setObjectName("preload_chbox")
        # # self.preload_chbox.pressed.connect(self.on_preload_chbox_click_slot)
        # self.preload_chbox.stateChanged.connect(self.on_preload_chbox_stateChanged_slot)
        # self.horizontalLayout_3.addWidget(self.preload_chbox)
        self.show_ids = QtWidgets.QCheckBox(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_ids.sizePolicy().hasHeightForWidth())
        self.show_ids.setSizePolicy(sizePolicy)
        self.show_ids.setObjectName("show_ids")
        self.show_ids.setChecked(True)
        self.show_ids.stateChanged.connect(self.on_show_ids_stateChanged_slot)
        self.horizontalLayout_3.addWidget(self.show_ids)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label = QtWidgets.QLabel(self.content)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.zoomSlider = QtWidgets.QSlider(self.content)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(21)
        self.zoomSlider.setPageStep(1)
        self.zoomSlider.setProperty("value", 11)
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.zoomSlider.setObjectName("zoomSlider")
        self.zoomSlider.valueChanged.connect(self.on_zoomSlider_valueChanged_slot)
        self.verticalLayout_3.addWidget(self.zoomSlider)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.content)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.content)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(self.content)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dockWidget.setWidget(self.content)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.toolBar.addAction(self.actionNew)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Properties"))
        self.source_path.setText(_translate("MainWindow", "Source Path:"))
        self.loadbtn.setText(_translate("MainWindow", "Select"))
        self.save_path.setText(_translate("MainWindow", "Save Path:"))
        self.choose_save_btn.setText(_translate("MainWindow", "Select"))
        self.preivous_btn.setText(_translate("MainWindow", "Previous (A)"))
        self.next_btn.setText(_translate("MainWindow", "Next (F)"))
        self.save_btn.setText(_translate("MainWindow", "Save (S)"))
        self.normal_btn.setText(_translate("MainWindow", "Normal (E)"))
        self.hiden_btn.setText(_translate("MainWindow", "Occlusion (R)"))
        self.miss_btn.setText(_translate("MainWindow", "Self-Occlusion (T)"))
        # self.delete_btn.setText(_translate("MainWindow", "Delete (D)"))
        # self.draw_oval_btn.setText(_translate("MainWindow", "Normal_oval (I)"))
        # self.draw_occlusion_oval_btn.setText(_translate("MainWindow", "occlusion_oval (O)"))
        # self.draw_self_occlusion_oval_btn.setText(_translate("MainWindow", "self_occlusion_oval (P)"))
        # self.preload_chbox.setText(_translate("MainWindow", "Preloading"))
        self.show_ids.setText(_translate("MainWindow", "id"))
        self.label.setText(_translate("MainWindow", "Zoom:"))
        self.label_4.setText(_translate("MainWindow", "10%"))
        self.label_3.setText(_translate("MainWindow", "100%"))
        self.label_2.setText(_translate("MainWindow", "200%"))
        self.actionNew.setText(_translate("MainWindow", "New"))

