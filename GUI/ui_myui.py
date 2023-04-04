# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'myui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGraphicsView, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QSpinBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1220, 939)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        MainWindow.setMouseTracking(False)
        self.actionnew = QAction(MainWindow)
        self.actionnew.setObjectName(u"actionnew")
        self.actionnew.setCheckable(False)
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SetNoConstraint)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy2)
        self.tab_calibration = QWidget()
        self.tab_calibration.setObjectName(u"tab_calibration")
        sizePolicy1.setHeightForWidth(self.tab_calibration.sizePolicy().hasHeightForWidth())
        self.tab_calibration.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.tab_calibration)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 9)
        self.label_5 = QLabel(self.tab_calibration)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_calibration)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy3.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy3)
        self.gridLayout_12 = QGridLayout(self.groupBox_5)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.doubleSpinBox_Rate2findSurface_tabTAF = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_Rate2findSurface_tabTAF.setObjectName(u"doubleSpinBox_Rate2findSurface_tabTAF")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Rate2findSurface_tabTAF.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Rate2findSurface_tabTAF.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Rate2findSurface_tabTAF.setDecimals(1)
        self.doubleSpinBox_Rate2findSurface_tabTAF.setValue(1.000000000000000)

        self.gridLayout_12.addWidget(self.doubleSpinBox_Rate2findSurface_tabTAF, 0, 1, 1, 1)

        self.checkBox_UsingRate2findSurface_tabTAF = QCheckBox(self.groupBox_5)
        self.checkBox_UsingRate2findSurface_tabTAF.setObjectName(u"checkBox_UsingRate2findSurface_tabTAF")
        sizePolicy.setHeightForWidth(self.checkBox_UsingRate2findSurface_tabTAF.sizePolicy().hasHeightForWidth())
        self.checkBox_UsingRate2findSurface_tabTAF.setSizePolicy(sizePolicy)
        self.checkBox_UsingRate2findSurface_tabTAF.setChecked(True)

        self.gridLayout_12.addWidget(self.checkBox_UsingRate2findSurface_tabTAF, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_5, 2, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_calibration)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy3.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy3)
        self.gridLayout_10 = QGridLayout(self.groupBox_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_10.addWidget(self.label, 2, 1, 1, 1)

        self.comboBox = QComboBox(self.groupBox_3)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)

        self.gridLayout_10.addWidget(self.comboBox, 2, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)
        self.label_2.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_10.addWidget(self.label_2, 1, 1, 1, 1)

        self.comboBox_method_tabCalibration = QComboBox(self.groupBox_3)
        self.comboBox_method_tabCalibration.addItem("")
        self.comboBox_method_tabCalibration.addItem("")
        self.comboBox_method_tabCalibration.addItem("")
        self.comboBox_method_tabCalibration.setObjectName(u"comboBox_method_tabCalibration")
        self.comboBox_method_tabCalibration.setEnabled(False)
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.comboBox_method_tabCalibration.sizePolicy().hasHeightForWidth())
        self.comboBox_method_tabCalibration.setSizePolicy(sizePolicy5)
        self.comboBox_method_tabCalibration.setMinimumSize(QSize(120, 0))
        self.comboBox_method_tabCalibration.setEditable(False)

        self.gridLayout_10.addWidget(self.comboBox_method_tabCalibration, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.OK_path_tabCalibration = QPushButton(self.tab_calibration)
        self.OK_path_tabCalibration.setObjectName(u"OK_path_tabCalibration")
        sizePolicy.setHeightForWidth(self.OK_path_tabCalibration.sizePolicy().hasHeightForWidth())
        self.OK_path_tabCalibration.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.OK_path_tabCalibration, 6, 1, 1, 1)

        self.progressBar_calibration = QProgressBar(self.tab_calibration)
        self.progressBar_calibration.setObjectName(u"progressBar_calibration")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.progressBar_calibration.sizePolicy().hasHeightForWidth())
        self.progressBar_calibration.setSizePolicy(sizePolicy6)
        self.progressBar_calibration.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar_calibration, 6, 2, 1, 2)

        self.groupBox = QGroupBox(self.tab_calibration)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy7)
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_32 = QLabel(self.groupBox)
        self.label_32.setObjectName(u"label_32")
        sizePolicy3.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy3)

        self.gridLayout_7.addWidget(self.label_32, 0, 0, 1, 1)

        self.lineEdit_MaterialName_tabTAF = QLineEdit(self.groupBox)
        self.lineEdit_MaterialName_tabTAF.setObjectName(u"lineEdit_MaterialName_tabTAF")
        sizePolicy8 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.lineEdit_MaterialName_tabTAF.sizePolicy().hasHeightForWidth())
        self.lineEdit_MaterialName_tabTAF.setSizePolicy(sizePolicy8)
        self.lineEdit_MaterialName_tabTAF.setMinimumSize(QSize(300, 0))

        self.gridLayout_7.addWidget(self.lineEdit_MaterialName_tabTAF, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.gridLayout_7.addWidget(self.label_4, 0, 2, 1, 1)

        self.doubleSpinBox_E_tabCalibration = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_E_tabCalibration.setObjectName(u"doubleSpinBox_E_tabCalibration")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_E_tabCalibration.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_E_tabCalibration.setSizePolicy(sizePolicy)
        self.doubleSpinBox_E_tabCalibration.setDecimals(3)
        self.doubleSpinBox_E_tabCalibration.setValue(72.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_E_tabCalibration, 0, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy9 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy9)

        self.gridLayout_7.addWidget(self.label_3, 0, 4, 1, 1)

        self.doubleSpinBox_Poisson_tabCalibration = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_Poisson_tabCalibration.setObjectName(u"doubleSpinBox_Poisson_tabCalibration")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Poisson_tabCalibration.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Poisson_tabCalibration.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Poisson_tabCalibration.setDecimals(4)
        self.doubleSpinBox_Poisson_tabCalibration.setValue(0.179000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_Poisson_tabCalibration, 0, 5, 1, 1)

        self.label_33 = QLabel(self.groupBox)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_33, 2, 0, 1, 1)

        self.frame_4 = QFrame(self.groupBox)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_4, 0, 6, 1, 1)

        self.lineEdit_path_tabCalibration = QLineEdit(self.groupBox)
        self.lineEdit_path_tabCalibration.setObjectName(u"lineEdit_path_tabCalibration")
        sizePolicy7.setHeightForWidth(self.lineEdit_path_tabCalibration.sizePolicy().hasHeightForWidth())
        self.lineEdit_path_tabCalibration.setSizePolicy(sizePolicy7)

        self.gridLayout_7.addWidget(self.lineEdit_path_tabCalibration, 2, 1, 1, 6)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 8)

        self.tableWidget_tabTAF = QTableWidget(self.tab_calibration)
        if (self.tableWidget_tabTAF.columnCount() < 2):
            self.tableWidget_tabTAF.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTAF.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTAF.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget_tabTAF.rowCount() < 1):
            self.tableWidget_tabTAF.setRowCount(1)
        self.tableWidget_tabTAF.setObjectName(u"tableWidget_tabTAF")
        sizePolicy10 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.tableWidget_tabTAF.sizePolicy().hasHeightForWidth())
        self.tableWidget_tabTAF.setSizePolicy(sizePolicy10)
        self.tableWidget_tabTAF.setMinimumSize(QSize(180, 0))
        self.tableWidget_tabTAF.setMaximumSize(QSize(200, 16777215))
        self.tableWidget_tabTAF.setAutoScroll(True)
        self.tableWidget_tabTAF.setRowCount(1)
        self.tableWidget_tabTAF.horizontalHeader().setVisible(True)
        self.tableWidget_tabTAF.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_tabTAF.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget_tabTAF.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_tabTAF.horizontalHeader().setProperty("showSortIndicator", True)

        self.gridLayout_2.addWidget(self.tableWidget_tabTAF, 15, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_calibration)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy11)
        self.gridLayout_9 = QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.gridLayout_9.addWidget(self.label_7, 0, 5, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(110, 0))

        self.gridLayout_9.addWidget(self.label_6, 0, 1, 1, 1)

        self.doubleSpinBox_End_Pmax_tabCalibration = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_End_Pmax_tabCalibration.setObjectName(u"doubleSpinBox_End_Pmax_tabCalibration")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_End_Pmax_tabCalibration.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_End_Pmax_tabCalibration.setSizePolicy(sizePolicy)
        self.doubleSpinBox_End_Pmax_tabCalibration.setValue(0.500000000000000)

        self.gridLayout_9.addWidget(self.doubleSpinBox_End_Pmax_tabCalibration, 0, 6, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.gridLayout_9.addWidget(self.label_9, 1, 5, 1, 1)

        self.doubleSpinBox_zeroGradDelta_tabCalibration = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_zeroGradDelta_tabCalibration.setObjectName(u"doubleSpinBox_zeroGradDelta_tabCalibration")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zeroGradDelta_tabCalibration.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zeroGradDelta_tabCalibration.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zeroGradDelta_tabCalibration.setDecimals(4)
        self.doubleSpinBox_zeroGradDelta_tabCalibration.setValue(0.003000000000000)

        self.gridLayout_9.addWidget(self.doubleSpinBox_zeroGradDelta_tabCalibration, 1, 4, 1, 1)

        self.doubleSpinBox_Start_Pmax_tabCalibration = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_Start_Pmax_tabCalibration.setObjectName(u"doubleSpinBox_Start_Pmax_tabCalibration")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Start_Pmax_tabCalibration.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Start_Pmax_tabCalibration.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Start_Pmax_tabCalibration.setValue(1.000000000000000)

        self.gridLayout_9.addWidget(self.doubleSpinBox_Start_Pmax_tabCalibration, 0, 4, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.gridLayout_9.addWidget(self.label_8, 1, 1, 1, 1)

        self.spinBox_min_size_fluctuation_tabCalibration = QSpinBox(self.groupBox_2)
        self.spinBox_min_size_fluctuation_tabCalibration.setObjectName(u"spinBox_min_size_fluctuation_tabCalibration")
        sizePolicy.setHeightForWidth(self.spinBox_min_size_fluctuation_tabCalibration.sizePolicy().hasHeightForWidth())
        self.spinBox_min_size_fluctuation_tabCalibration.setSizePolicy(sizePolicy)
        self.spinBox_min_size_fluctuation_tabCalibration.setValue(1)

        self.gridLayout_9.addWidget(self.spinBox_min_size_fluctuation_tabCalibration, 1, 6, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_2, 2, 2, 1, 1)

        self.groupBox_6 = QGroupBox(self.tab_calibration)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.gridLayout_14 = QGridLayout(self.groupBox_6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_12 = QLabel(self.groupBox_6)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_14.addWidget(self.label_12, 0, 0, 1, 1)

        self.doubleSpinBox_critDepthStiffness_tabCalibration = QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_critDepthStiffness_tabCalibration.setObjectName(u"doubleSpinBox_critDepthStiffness_tabCalibration")
        self.doubleSpinBox_critDepthStiffness_tabCalibration.setValue(0.100000000000000)

        self.gridLayout_14.addWidget(self.doubleSpinBox_critDepthStiffness_tabCalibration, 0, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_14.addWidget(self.label_13, 1, 0, 1, 1)

        self.doubleSpinBox_critForceStiffness_tabCalibration = QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_critForceStiffness_tabCalibration.setObjectName(u"doubleSpinBox_critForceStiffness_tabCalibration")
        self.doubleSpinBox_critForceStiffness_tabCalibration.setValue(10.000000000000000)

        self.gridLayout_14.addWidget(self.doubleSpinBox_critForceStiffness_tabCalibration, 1, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_6, 2, 3, 1, 1)

        self.groupBox_7 = QGroupBox(self.tab_calibration)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy11.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy11)
        self.gridLayout_15 = QGridLayout(self.groupBox_7)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.doubleSpinBox_E_Tip_tabTAF = QDoubleSpinBox(self.groupBox_7)
        self.doubleSpinBox_E_Tip_tabTAF.setObjectName(u"doubleSpinBox_E_Tip_tabTAF")
        self.doubleSpinBox_E_Tip_tabTAF.setDecimals(3)
        self.doubleSpinBox_E_Tip_tabTAF.setMaximum(99999.990000000005239)
        self.doubleSpinBox_E_Tip_tabTAF.setValue(1141.000000000000000)

        self.gridLayout_15.addWidget(self.doubleSpinBox_E_Tip_tabTAF, 0, 3, 1, 1)

        self.spinBox_number_of_TAFterms = QSpinBox(self.groupBox_7)
        self.spinBox_number_of_TAFterms.setObjectName(u"spinBox_number_of_TAFterms")
        sizePolicy11.setHeightForWidth(self.spinBox_number_of_TAFterms.sizePolicy().hasHeightForWidth())
        self.spinBox_number_of_TAFterms.setSizePolicy(sizePolicy11)
        self.spinBox_number_of_TAFterms.setValue(3)

        self.gridLayout_15.addWidget(self.spinBox_number_of_TAFterms, 0, 7, 1, 1)

        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName(u"label_14")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy12)

        self.gridLayout_15.addWidget(self.label_14, 0, 6, 1, 1)

        self.lineEdit_TipName_tabTAF = QLineEdit(self.groupBox_7)
        self.lineEdit_TipName_tabTAF.setObjectName(u"lineEdit_TipName_tabTAF")
        sizePolicy6.setHeightForWidth(self.lineEdit_TipName_tabTAF.sizePolicy().hasHeightForWidth())
        self.lineEdit_TipName_tabTAF.setSizePolicy(sizePolicy6)

        self.gridLayout_15.addWidget(self.lineEdit_TipName_tabTAF, 0, 1, 1, 1)

        self.label_34 = QLabel(self.groupBox_7)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_15.addWidget(self.label_34, 0, 2, 1, 1)

        self.label_63 = QLabel(self.groupBox_7)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_15.addWidget(self.label_63, 0, 0, 1, 1)

        self.label_64 = QLabel(self.groupBox_7)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_15.addWidget(self.label_64, 0, 4, 1, 1)

        self.doubleSpinBox_Poisson_Tip_tabTAF = QDoubleSpinBox(self.groupBox_7)
        self.doubleSpinBox_Poisson_Tip_tabTAF.setObjectName(u"doubleSpinBox_Poisson_Tip_tabTAF")
        self.doubleSpinBox_Poisson_Tip_tabTAF.setDecimals(3)
        self.doubleSpinBox_Poisson_Tip_tabTAF.setValue(0.070000000000000)

        self.gridLayout_15.addWidget(self.doubleSpinBox_Poisson_Tip_tabTAF, 0, 5, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_7, 1, 0, 1, 4)

        self.frame = QFrame(self.tab_calibration)
        self.frame.setObjectName(u"frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_52 = QGridLayout(self.frame)
        self.gridLayout_52.setObjectName(u"gridLayout_52")

        self.gridLayout_2.addWidget(self.frame, 2, 4, 1, 4)

        self.graphicsView_tab_TipAreaFunction = QTabWidget(self.tab_calibration)
        self.graphicsView_tab_TipAreaFunction.setObjectName(u"graphicsView_tab_TipAreaFunction")
        sizePolicy13 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.graphicsView_tab_TipAreaFunction.sizePolicy().hasHeightForWidth())
        self.graphicsView_tab_TipAreaFunction.setSizePolicy(sizePolicy13)
        self.graphicsView_tab_TipAreaFunction.setUsesScrollButtons(True)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tabWidget_3 = QTabWidget(self.tab_3)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_6 = QGridLayout(self.tab_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTAF = QCheckBox(self.tab_5)
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTAF.setObjectName(u"checkBox_iLHU_inclusive_frame_stiffness_tabTAF")

        self.gridLayout_6.addWidget(self.checkBox_iLHU_inclusive_frame_stiffness_tabTAF, 2, 3, 1, 1)

        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF = QGraphicsView(self.tab_5)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setObjectName(u"graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF")
        sizePolicy2.setHeightForWidth(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setSizePolicy(sizePolicy2)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setMinimumSize(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setMaximumSize(QSize(16777215, 16777215))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setSizeIncrement(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setBaseSize(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_6.addWidget(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTAF, 1, 0, 1, 5)

        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness = QPushButton(self.tab_5)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness")
        sizePolicy.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness, 2, 1, 1, 1)

        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTAF = QCheckBox(self.tab_5)
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTAF.setObjectName(u"checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTAF")

        self.gridLayout_6.addWidget(self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTAF, 2, 2, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_8 = QGridLayout(self.tab_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF = QGraphicsView(self.tab_6)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF")
        sizePolicy1.setHeightForWidth(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")

        self.gridLayout_5.addWidget(self.tabWidget_3, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction.addTab(self.tab_3, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)

        self.graphicsView_tabFrameStiffness = QGraphicsView(self.tab)
        self.graphicsView_tabFrameStiffness.setObjectName(u"graphicsView_tabFrameStiffness")

        self.gridLayout.addWidget(self.graphicsView_tabFrameStiffness, 4, 0, 1, 7)

        self.lineEdit_FrameStiffness_Calibration = QLineEdit(self.tab)
        self.lineEdit_FrameStiffness_Calibration.setObjectName(u"lineEdit_FrameStiffness_Calibration")
        self.lineEdit_FrameStiffness_Calibration.setEnabled(True)
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameStiffness_Calibration.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameStiffness_Calibration.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameStiffness_Calibration.setFrame(True)
        self.lineEdit_FrameStiffness_Calibration.setDragEnabled(False)
        self.lineEdit_FrameStiffness_Calibration.setReadOnly(True)
        self.lineEdit_FrameStiffness_Calibration.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.lineEdit_FrameStiffness_Calibration, 2, 1, 1, 1)

        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 2, 2, 1, 1)

        self.lineEdit_FrameCompliance_Calibration = QLineEdit(self.tab)
        self.lineEdit_FrameCompliance_Calibration.setObjectName(u"lineEdit_FrameCompliance_Calibration")
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameCompliance_Calibration.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameCompliance_Calibration.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameCompliance_Calibration.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_FrameCompliance_Calibration, 2, 3, 1, 1)

        self.graphicsView_tab_TipAreaFunction.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_13 = QGridLayout(self.tab_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.graphicsView_tabTipAreaFunction = QGraphicsView(self.tab_2)
        self.graphicsView_tabTipAreaFunction.setObjectName(u"graphicsView_tabTipAreaFunction")
        sizePolicy14 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy14.setHorizontalStretch(100)
        sizePolicy14.setVerticalStretch(100)
        sizePolicy14.setHeightForWidth(self.graphicsView_tabTipAreaFunction.sizePolicy().hasHeightForWidth())
        self.graphicsView_tabTipAreaFunction.setSizePolicy(sizePolicy14)

        self.gridLayout_13.addWidget(self.graphicsView_tabTipAreaFunction, 2, 0, 1, 12)

        self.groupBox_22 = QGroupBox(self.tab_2)
        self.groupBox_22.setObjectName(u"groupBox_22")
        sizePolicy13.setHeightForWidth(self.groupBox_22.sizePolicy().hasHeightForWidth())
        self.groupBox_22.setSizePolicy(sizePolicy13)
        self.groupBox_22.setMinimumSize(QSize(800, 0))
        self.gridLayout_42 = QGridLayout(self.groupBox_22)
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.label_30 = QLabel(self.groupBox_22)
        self.label_30.setObjectName(u"label_30")
        sizePolicy3.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_30, 0, 8, 1, 1)

        self.label_29 = QLabel(self.groupBox_22)
        self.label_29.setObjectName(u"label_29")
        sizePolicy3.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_29, 0, 6, 1, 1)

        self.lineEdit_TAF1_tabTAF = QLineEdit(self.groupBox_22)
        self.lineEdit_TAF1_tabTAF.setObjectName(u"lineEdit_TAF1_tabTAF")
        self.lineEdit_TAF1_tabTAF.setReadOnly(True)

        self.gridLayout_42.addWidget(self.lineEdit_TAF1_tabTAF, 0, 1, 1, 1)

        self.lineEdit_TAF4_tabTAF = QLineEdit(self.groupBox_22)
        self.lineEdit_TAF4_tabTAF.setObjectName(u"lineEdit_TAF4_tabTAF")
        self.lineEdit_TAF4_tabTAF.setReadOnly(True)

        self.gridLayout_42.addWidget(self.lineEdit_TAF4_tabTAF, 0, 7, 1, 1)

        self.label_28 = QLabel(self.groupBox_22)
        self.label_28.setObjectName(u"label_28")
        sizePolicy3.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_28, 0, 4, 1, 1)

        self.label_26 = QLabel(self.groupBox_22)
        self.label_26.setObjectName(u"label_26")
        sizePolicy3.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_26, 0, 0, 1, 1)

        self.lineEdit_TAF5_tabTAF = QLineEdit(self.groupBox_22)
        self.lineEdit_TAF5_tabTAF.setObjectName(u"lineEdit_TAF5_tabTAF")
        self.lineEdit_TAF5_tabTAF.setReadOnly(True)

        self.gridLayout_42.addWidget(self.lineEdit_TAF5_tabTAF, 0, 9, 1, 1)

        self.lineEdit_TAF3_tabTAF = QLineEdit(self.groupBox_22)
        self.lineEdit_TAF3_tabTAF.setObjectName(u"lineEdit_TAF3_tabTAF")
        self.lineEdit_TAF3_tabTAF.setReadOnly(True)

        self.gridLayout_42.addWidget(self.lineEdit_TAF3_tabTAF, 0, 5, 1, 1)

        self.label_27 = QLabel(self.groupBox_22)
        self.label_27.setObjectName(u"label_27")
        sizePolicy3.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_27, 0, 2, 1, 1)

        self.lineEdit_TAF2_tabTAF = QLineEdit(self.groupBox_22)
        self.lineEdit_TAF2_tabTAF.setObjectName(u"lineEdit_TAF2_tabTAF")
        self.lineEdit_TAF2_tabTAF.setReadOnly(True)

        self.gridLayout_42.addWidget(self.lineEdit_TAF2_tabTAF, 0, 3, 1, 1)

        self.label_31 = QLabel(self.groupBox_22)
        self.label_31.setObjectName(u"label_31")
        sizePolicy3.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy3)

        self.gridLayout_42.addWidget(self.label_31, 0, 10, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_22, 1, 0, 1, 5)

        self.graphicsView_tab_TipAreaFunction.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.graphicsView_tab_TipAreaFunction, 15, 1, 1, 7)

        self.tabWidget.addTab(self.tab_calibration, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_16 = QGridLayout(self.tab_4)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.tabWidget_2 = QTabWidget(self.tab_4)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        sizePolicy15 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy15)
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_19 = QGridLayout(self.tab_7)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.graphicsView_tab_TipAreaFunction_2 = QTabWidget(self.tab_7)
        self.graphicsView_tab_TipAreaFunction_2.setObjectName(u"graphicsView_tab_TipAreaFunction_2")
        sizePolicy16 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.graphicsView_tab_TipAreaFunction_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_tab_TipAreaFunction_2.setSizePolicy(sizePolicy16)
        self.graphicsView_tab_TipAreaFunction_2.setUsesScrollButtons(True)
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_20 = QGridLayout(self.tab_9)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.tabWidget_4 = QTabWidget(self.tab_9)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_21 = QGridLayout(self.tab_10)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius_FrameStiffness = QCheckBox(self.tab_10)
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setObjectName(u"checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius_FrameStiffness")

        self.gridLayout_21.addWidget(self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius_FrameStiffness, 2, 3, 1, 1)

        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness = QGraphicsView(self.tab_10)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setObjectName(u"graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness")
        sizePolicy4.setHeightForWidth(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy4)

        self.gridLayout_21.addWidget(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness, 1, 0, 1, 4)

        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness = QPushButton(self.tab_10)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness")
        sizePolicy7.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy7)

        self.gridLayout_21.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness, 2, 1, 1, 1)

        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness = QCheckBox(self.tab_10)
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setObjectName(u"checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness")

        self.gridLayout_21.addWidget(self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness, 2, 2, 1, 1)

        self.tabWidget_4.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_22 = QGridLayout(self.tab_11)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_2 = QGraphicsView(self.tab_11)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_2.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_2")
        sizePolicy1.setHeightForWidth(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_2.setSizePolicy(sizePolicy1)

        self.gridLayout_22.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_2, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_11, "")

        self.gridLayout_20.addWidget(self.tabWidget_4, 1, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_2.addTab(self.tab_9, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_23 = QGridLayout(self.tab_12)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.label_19 = QLabel(self.tab_12)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_23.addWidget(self.label_19, 1, 2, 1, 1)

        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness = QLineEdit(self.tab_12)
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setObjectName(u"lineEdit_FrameStiffness_tabTipRadius_FrameStiffness")
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setEnabled(True)
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setFrame(True)
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setDragEnabled(False)
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setReadOnly(True)
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setClearButtonEnabled(False)

        self.gridLayout_23.addWidget(self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness, 1, 1, 1, 1)

        self.label_20 = QLabel(self.tab_12)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_23.addWidget(self.label_20, 1, 0, 1, 1)

        self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness = QLineEdit(self.tab_12)
        self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness.setObjectName(u"lineEdit_FrameCompliance_tabTipRadius_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness.setReadOnly(True)

        self.gridLayout_23.addWidget(self.lineEdit_FrameCompliance_tabTipRadius_FrameStiffness, 1, 3, 1, 1)

        self.graphicsView_tabTipRadius_FrameStiffness = QGraphicsView(self.tab_12)
        self.graphicsView_tabTipRadius_FrameStiffness.setObjectName(u"graphicsView_tabTipRadius_FrameStiffness")
        self.graphicsView_tabTipRadius_FrameStiffness.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_23.addWidget(self.graphicsView_tabTipRadius_FrameStiffness, 3, 0, 1, 6)

        self.graphicsView_tab_TipAreaFunction_2.addTab(self.tab_12, "")

        self.gridLayout_19.addWidget(self.graphicsView_tab_TipAreaFunction_2, 11, 1, 1, 10)

        self.groupBox_10 = QGroupBox(self.tab_7)
        self.groupBox_10.setObjectName(u"groupBox_10")
        sizePolicy3.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy3)
        self.groupBox_10.setMinimumSize(QSize(0, 0))
        self.gridLayout_18 = QGridLayout(self.groupBox_10)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_15 = QLabel(self.groupBox_10)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(0, 0))

        self.gridLayout_18.addWidget(self.label_15, 0, 5, 1, 1)

        self.label_18 = QLabel(self.groupBox_10)
        self.label_18.setObjectName(u"label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QSize(0, 0))

        self.gridLayout_18.addWidget(self.label_18, 1, 5, 1, 1)

        self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness.setValue(0.500000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_End_Pmax_tabTipRadius_FrameStiffness, 0, 6, 1, 1)

        self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness = QSpinBox(self.groupBox_10)
        self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness.setObjectName(u"spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness")
        sizePolicy.setHeightForWidth(self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy)
        self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness.setValue(1)

        self.gridLayout_18.addWidget(self.spinBox_min_size_fluctuation_tabTipRadius_FrameStiffness, 1, 6, 1, 1)

        self.label_17 = QLabel(self.groupBox_10)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.gridLayout_18.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_10)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QSize(110, 0))

        self.gridLayout_18.addWidget(self.label_16, 0, 0, 1, 1)

        self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness.setValue(1.000000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_Start_Pmax_tabTipRadius_FrameStiffness, 0, 4, 1, 1)

        self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness.setDecimals(4)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness.setValue(0.010000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_zeroGradDelta_tabTipRadius_FrameStiffness, 1, 4, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_10, 3, 2, 1, 1)

        self.groupBox_11 = QGroupBox(self.tab_7)
        self.groupBox_11.setObjectName(u"groupBox_11")
        sizePolicy3.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy3)
        self.gridLayout_25 = QGridLayout(self.groupBox_11)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.label_23 = QLabel(self.groupBox_11)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)
        self.label_23.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_25.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_11)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_25.addWidget(self.label_22, 2, 1, 1, 1)

        self.comboBox_Equipment_tabTipRadius_FrameStiffness = QComboBox(self.groupBox_11)
        self.comboBox_Equipment_tabTipRadius_FrameStiffness.addItem("")
        self.comboBox_Equipment_tabTipRadius_FrameStiffness.setObjectName(u"comboBox_Equipment_tabTipRadius_FrameStiffness")
        self.comboBox_Equipment_tabTipRadius_FrameStiffness.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.comboBox_Equipment_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.comboBox_Equipment_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)

        self.gridLayout_25.addWidget(self.comboBox_Equipment_tabTipRadius_FrameStiffness, 2, 2, 1, 1)

        self.comboBox_method_tabTipRadius_FrameStiffness = QComboBox(self.groupBox_11)
        self.comboBox_method_tabTipRadius_FrameStiffness.addItem("")
        self.comboBox_method_tabTipRadius_FrameStiffness.addItem("")
        self.comboBox_method_tabTipRadius_FrameStiffness.addItem("")
        self.comboBox_method_tabTipRadius_FrameStiffness.setObjectName(u"comboBox_method_tabTipRadius_FrameStiffness")
        self.comboBox_method_tabTipRadius_FrameStiffness.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.comboBox_method_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.comboBox_method_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy5)
        self.comboBox_method_tabTipRadius_FrameStiffness.setMinimumSize(QSize(120, 0))
        self.comboBox_method_tabTipRadius_FrameStiffness.setEditable(False)

        self.gridLayout_25.addWidget(self.comboBox_method_tabTipRadius_FrameStiffness, 1, 2, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_11, 3, 0, 1, 1)

        self.tableWidget_tabTipRadius_FrameStiffness = QTableWidget(self.tab_7)
        if (self.tableWidget_tabTipRadius_FrameStiffness.columnCount() < 2):
            self.tableWidget_tabTipRadius_FrameStiffness.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTipRadius_FrameStiffness.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTipRadius_FrameStiffness.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        if (self.tableWidget_tabTipRadius_FrameStiffness.rowCount() < 1):
            self.tableWidget_tabTipRadius_FrameStiffness.setRowCount(1)
        self.tableWidget_tabTipRadius_FrameStiffness.setObjectName(u"tableWidget_tabTipRadius_FrameStiffness")
        sizePolicy10.setHeightForWidth(self.tableWidget_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.tableWidget_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy10)
        self.tableWidget_tabTipRadius_FrameStiffness.setMinimumSize(QSize(0, 0))
        self.tableWidget_tabTipRadius_FrameStiffness.setMaximumSize(QSize(200, 16777215))
        self.tableWidget_tabTipRadius_FrameStiffness.setAutoScroll(True)
        self.tableWidget_tabTipRadius_FrameStiffness.setRowCount(1)
        self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeader().setVisible(True)
        self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeader().setHighlightSections(True)
        self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeader().setProperty("showSortIndicator", True)

        self.gridLayout_19.addWidget(self.tableWidget_tabTipRadius_FrameStiffness, 11, 0, 1, 1)

        self.pushButton_Calculate_tabTipRadius_FrameStiffness = QPushButton(self.tab_7)
        self.pushButton_Calculate_tabTipRadius_FrameStiffness.setObjectName(u"pushButton_Calculate_tabTipRadius_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.pushButton_Calculate_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.pushButton_Calculate_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)

        self.gridLayout_19.addWidget(self.pushButton_Calculate_tabTipRadius_FrameStiffness, 5, 1, 1, 1)

        self.label_21 = QLabel(self.tab_7)
        self.label_21.setObjectName(u"label_21")
        sizePolicy3.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy3)

        self.gridLayout_19.addWidget(self.label_21, 5, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.tab_7)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy3.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy3)
        self.gridLayout_26 = QGridLayout(self.groupBox_12)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness.setValue(0.100000000000000)

        self.gridLayout_26.addWidget(self.doubleSpinBox_critDepthStiffness_tabTipRadius_FrameStiffness, 0, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox_12)
        self.label_24.setObjectName(u"label_24")
        sizePolicy3.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy3)

        self.gridLayout_26.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_25 = QLabel(self.groupBox_12)
        self.label_25.setObjectName(u"label_25")
        sizePolicy3.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy3)

        self.gridLayout_26.addWidget(self.label_25, 1, 0, 1, 1)

        self.doubleSpinBox_critForceStiffness_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_critForceStiffness_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_critForceStiffness_tabTipRadius_FrameStiffness")
        self.doubleSpinBox_critForceStiffness_tabTipRadius_FrameStiffness.setValue(8.000000000000000)

        self.gridLayout_26.addWidget(self.doubleSpinBox_critForceStiffness_tabTipRadius_FrameStiffness, 1, 1, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_12, 3, 3, 1, 1)

        self.frame_2 = QFrame(self.tab_7)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout_19.addWidget(self.frame_2, 3, 4, 1, 7)

        self.groupBox_8 = QGroupBox(self.tab_7)
        self.groupBox_8.setObjectName(u"groupBox_8")
        sizePolicy3.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy3)
        self.groupBox_8.setMinimumSize(QSize(253, 0))
        self.groupBox_8.setMaximumSize(QSize(253, 16777215))
        self.gridLayout_24 = QGridLayout(self.groupBox_8)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness = QDoubleSpinBox(self.groupBox_8)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness.setObjectName(u"doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness.setDecimals(1)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness.setValue(1.000000000000000)

        self.gridLayout_24.addWidget(self.doubleSpinBox_Rate2findSurface_tabTipRadius_FrameStiffness, 0, 1, 1, 1)

        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness = QCheckBox(self.groupBox_8)
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setObjectName(u"checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy8)
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setMinimumSize(QSize(0, 0))
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setChecked(True)

        self.gridLayout_24.addWidget(self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_8, 3, 1, 1, 1)

        self.groupBox_9 = QGroupBox(self.tab_7)
        self.groupBox_9.setObjectName(u"groupBox_9")
        sizePolicy7.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy7)
        self.gridLayout_17 = QGridLayout(self.groupBox_9)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.lineEdit_path_tabTipRadius_FrameStiffness = QLineEdit(self.groupBox_9)
        self.lineEdit_path_tabTipRadius_FrameStiffness.setObjectName(u"lineEdit_path_tabTipRadius_FrameStiffness")
        sizePolicy17 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.lineEdit_path_tabTipRadius_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_path_tabTipRadius_FrameStiffness.setSizePolicy(sizePolicy17)

        self.gridLayout_17.addWidget(self.lineEdit_path_tabTipRadius_FrameStiffness, 0, 1, 1, 1)


        self.gridLayout_19.addWidget(self.groupBox_9, 0, 0, 1, 11)

        self.progressBar_tabTipRadius_FrameStiffness = QProgressBar(self.tab_7)
        self.progressBar_tabTipRadius_FrameStiffness.setObjectName(u"progressBar_tabTipRadius_FrameStiffness")
        self.progressBar_tabTipRadius_FrameStiffness.setValue(0)

        self.gridLayout_19.addWidget(self.progressBar_tabTipRadius_FrameStiffness, 5, 2, 1, 2)

        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_65 = QGridLayout(self.tab_8)
        self.gridLayout_65.setObjectName(u"gridLayout_65")
        self.groupBox_29 = QGroupBox(self.tab_8)
        self.groupBox_29.setObjectName(u"groupBox_29")
        sizePolicy5.setHeightForWidth(self.groupBox_29.sizePolicy().hasHeightForWidth())
        self.groupBox_29.setSizePolicy(sizePolicy5)
        self.gridLayout_60 = QGridLayout(self.groupBox_29)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.frame_8 = QFrame(self.groupBox_29)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.gridLayout_60.addWidget(self.frame_8, 0, 8, 1, 1)

        self.label_73 = QLabel(self.groupBox_29)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_60.addWidget(self.label_73, 1, 0, 1, 1)

        self.label_75 = QLabel(self.groupBox_29)
        self.label_75.setObjectName(u"label_75")
        sizePolicy3.setHeightForWidth(self.label_75.sizePolicy().hasHeightForWidth())
        self.label_75.setSizePolicy(sizePolicy3)

        self.gridLayout_60.addWidget(self.label_75, 0, 0, 1, 1)

        self.label_83 = QLabel(self.groupBox_29)
        self.label_83.setObjectName(u"label_83")
        sizePolicy.setHeightForWidth(self.label_83.sizePolicy().hasHeightForWidth())
        self.label_83.setSizePolicy(sizePolicy)

        self.gridLayout_60.addWidget(self.label_83, 0, 2, 1, 1)

        self.doubleSpinBox_Poisson_tabTipRadius = QDoubleSpinBox(self.groupBox_29)
        self.doubleSpinBox_Poisson_tabTipRadius.setObjectName(u"doubleSpinBox_Poisson_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_Poisson_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Poisson_tabTipRadius.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_Poisson_tabTipRadius.setDecimals(3)
        self.doubleSpinBox_Poisson_tabTipRadius.setValue(0.280000000000000)

        self.gridLayout_60.addWidget(self.doubleSpinBox_Poisson_tabTipRadius, 0, 5, 1, 1)

        self.frame_7 = QFrame(self.groupBox_29)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy3.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy3)
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.gridLayout_60.addWidget(self.frame_7, 0, 9, 1, 1)

        self.label_74 = QLabel(self.groupBox_29)
        self.label_74.setObjectName(u"label_74")
        sizePolicy3.setHeightForWidth(self.label_74.sizePolicy().hasHeightForWidth())
        self.label_74.setSizePolicy(sizePolicy3)

        self.gridLayout_60.addWidget(self.label_74, 0, 4, 1, 1)

        self.lineEdit_path_tabTipRadius = QLineEdit(self.groupBox_29)
        self.lineEdit_path_tabTipRadius.setObjectName(u"lineEdit_path_tabTipRadius")
        sizePolicy7.setHeightForWidth(self.lineEdit_path_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_path_tabTipRadius.setSizePolicy(sizePolicy7)

        self.gridLayout_60.addWidget(self.lineEdit_path_tabTipRadius, 1, 1, 1, 9)

        self.lineEdit_MaterialName_tabTipRadius = QLineEdit(self.groupBox_29)
        self.lineEdit_MaterialName_tabTipRadius.setObjectName(u"lineEdit_MaterialName_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.lineEdit_MaterialName_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_MaterialName_tabTipRadius.setSizePolicy(sizePolicy8)
        self.lineEdit_MaterialName_tabTipRadius.setMinimumSize(QSize(300, 0))

        self.gridLayout_60.addWidget(self.lineEdit_MaterialName_tabTipRadius, 0, 1, 1, 1)

        self.doubleSpinBox_E_tabTipRadius = QDoubleSpinBox(self.groupBox_29)
        self.doubleSpinBox_E_tabTipRadius.setObjectName(u"doubleSpinBox_E_tabTipRadius")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_E_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_E_tabTipRadius.setSizePolicy(sizePolicy)
        self.doubleSpinBox_E_tabTipRadius.setDecimals(2)
        self.doubleSpinBox_E_tabTipRadius.setMaximum(9999.000000000000000)
        self.doubleSpinBox_E_tabTipRadius.setValue(400.000000000000000)

        self.gridLayout_60.addWidget(self.doubleSpinBox_E_tabTipRadius, 0, 3, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_29, 0, 0, 1, 11)

        self.groupBox_27 = QGroupBox(self.tab_8)
        self.groupBox_27.setObjectName(u"groupBox_27")
        sizePolicy3.setHeightForWidth(self.groupBox_27.sizePolicy().hasHeightForWidth())
        self.groupBox_27.setSizePolicy(sizePolicy3)
        self.gridLayout_58 = QGridLayout(self.groupBox_27)
        self.gridLayout_58.setObjectName(u"gridLayout_58")
        self.checkBox_UsingRate2findSurface_tabTipRadius = QCheckBox(self.groupBox_27)
        self.checkBox_UsingRate2findSurface_tabTipRadius.setObjectName(u"checkBox_UsingRate2findSurface_tabTipRadius")
        sizePolicy.setHeightForWidth(self.checkBox_UsingRate2findSurface_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.checkBox_UsingRate2findSurface_tabTipRadius.setSizePolicy(sizePolicy)
        self.checkBox_UsingRate2findSurface_tabTipRadius.setChecked(True)

        self.gridLayout_58.addWidget(self.checkBox_UsingRate2findSurface_tabTipRadius, 0, 1, 1, 1)

        self.doubleSpinBox_Rate2findSurface_tabTipRadius = QDoubleSpinBox(self.groupBox_27)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius.setObjectName(u"doubleSpinBox_Rate2findSurface_tabTipRadius")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Rate2findSurface_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Rate2findSurface_tabTipRadius.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius.setDecimals(1)
        self.doubleSpinBox_Rate2findSurface_tabTipRadius.setValue(1.000000000000000)

        self.gridLayout_58.addWidget(self.doubleSpinBox_Rate2findSurface_tabTipRadius, 0, 2, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_27, 2, 2, 1, 1)

        self.graphicsView_tab_TipAreaFunction_5 = QTabWidget(self.tab_8)
        self.graphicsView_tab_TipAreaFunction_5.setObjectName(u"graphicsView_tab_TipAreaFunction_5")
        sizePolicy1.setHeightForWidth(self.graphicsView_tab_TipAreaFunction_5.sizePolicy().hasHeightForWidth())
        self.graphicsView_tab_TipAreaFunction_5.setSizePolicy(sizePolicy1)
        self.graphicsView_tab_TipAreaFunction_5.setUsesScrollButtons(True)
        self.tab_29 = QWidget()
        self.tab_29.setObjectName(u"tab_29")
        self.gridLayout_61 = QGridLayout(self.tab_29)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.tabWidget_9 = QTabWidget(self.tab_29)
        self.tabWidget_9.setObjectName(u"tabWidget_9")
        sizePolicy4.setHeightForWidth(self.tabWidget_9.sizePolicy().hasHeightForWidth())
        self.tabWidget_9.setSizePolicy(sizePolicy4)
        self.tab_30 = QWidget()
        self.tab_30.setObjectName(u"tab_30")
        self.gridLayout_62 = QGridLayout(self.tab_30)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius = QCheckBox(self.tab_30)
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius.setObjectName(u"checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius")

        self.gridLayout_62.addWidget(self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius, 2, 3, 1, 1)

        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius = QGraphicsView(self.tab_30)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setObjectName(u"graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius")
        sizePolicy2.setHeightForWidth(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setSizePolicy(sizePolicy2)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setMinimumSize(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setMaximumSize(QSize(16777215, 16777215))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setSizeIncrement(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setBaseSize(QSize(0, 0))
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_62.addWidget(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabTipRadius, 1, 0, 1, 5)

        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius = QPushButton(self.tab_30)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius")
        sizePolicy.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius.setSizePolicy(sizePolicy)

        self.gridLayout_62.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius, 2, 1, 1, 1)

        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius = QCheckBox(self.tab_30)
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius.setObjectName(u"checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius")

        self.gridLayout_62.addWidget(self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius, 2, 2, 1, 1)

        self.tabWidget_9.addTab(self.tab_30, "")
        self.tab_31 = QWidget()
        self.tab_31.setObjectName(u"tab_31")
        self.gridLayout_63 = QGridLayout(self.tab_31)
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2 = QGraphicsView(self.tab_31)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2")
        sizePolicy1.setHeightForWidth(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2.setSizePolicy(sizePolicy1)

        self.gridLayout_63.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabTAF_2, 0, 0, 1, 1)

        self.tabWidget_9.addTab(self.tab_31, "")

        self.gridLayout_61.addWidget(self.tabWidget_9, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_5.addTab(self.tab_29, "")
        self.tab_32 = QWidget()
        self.tab_32.setObjectName(u"tab_32")
        self.gridLayout_64 = QGridLayout(self.tab_32)
        self.gridLayout_64.setObjectName(u"gridLayout_64")
        self.frame_10 = QFrame(self.tab_32)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)

        self.gridLayout_64.addWidget(self.frame_10, 1, 0, 1, 1)

        self.graphicsView_HertzianFitting_tabTipRadius = QGraphicsView(self.tab_32)
        self.graphicsView_HertzianFitting_tabTipRadius.setObjectName(u"graphicsView_HertzianFitting_tabTipRadius")

        self.gridLayout_64.addWidget(self.graphicsView_HertzianFitting_tabTipRadius, 1, 1, 1, 1)

        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2 = QPushButton(self.tab_32)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2")
        sizePolicy.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2.setSizePolicy(sizePolicy)

        self.gridLayout_64.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2, 2, 1, 1, 1)

        self.graphicsView_tab_TipAreaFunction_5.addTab(self.tab_32, "")
        self.tab_33 = QWidget()
        self.tab_33.setObjectName(u"tab_33")
        self.gridLayout_66 = QGridLayout(self.tab_33)
        self.gridLayout_66.setObjectName(u"gridLayout_66")
        self.label_80 = QLabel(self.tab_33)
        self.label_80.setObjectName(u"label_80")
        sizePolicy.setHeightForWidth(self.label_80.sizePolicy().hasHeightForWidth())
        self.label_80.setSizePolicy(sizePolicy)

        self.gridLayout_66.addWidget(self.label_80, 0, 0, 1, 1)

        self.lineEdit_reducedModulus_tabTipRadius = QLineEdit(self.tab_33)
        self.lineEdit_reducedModulus_tabTipRadius.setObjectName(u"lineEdit_reducedModulus_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.lineEdit_reducedModulus_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_reducedModulus_tabTipRadius.setSizePolicy(sizePolicy8)
        self.lineEdit_reducedModulus_tabTipRadius.setReadOnly(True)

        self.gridLayout_66.addWidget(self.lineEdit_reducedModulus_tabTipRadius, 0, 5, 1, 1)

        self.label_84 = QLabel(self.tab_33)
        self.label_84.setObjectName(u"label_84")
        sizePolicy3.setHeightForWidth(self.label_84.sizePolicy().hasHeightForWidth())
        self.label_84.setSizePolicy(sizePolicy3)

        self.gridLayout_66.addWidget(self.label_84, 0, 2, 1, 1)

        self.label_81 = QLabel(self.tab_33)
        self.label_81.setObjectName(u"label_81")

        self.gridLayout_66.addWidget(self.label_81, 0, 4, 1, 1)

        self.lineEdit_TipRadius_tabTipRadius = QLineEdit(self.tab_33)
        self.lineEdit_TipRadius_tabTipRadius.setObjectName(u"lineEdit_TipRadius_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.lineEdit_TipRadius_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_TipRadius_tabTipRadius.setSizePolicy(sizePolicy8)
        self.lineEdit_TipRadius_tabTipRadius.setReadOnly(True)

        self.gridLayout_66.addWidget(self.lineEdit_TipRadius_tabTipRadius, 0, 1, 1, 1)

        self.graphicsView_CalculatedTipRadius_tabTipRadius = QGraphicsView(self.tab_33)
        self.graphicsView_CalculatedTipRadius_tabTipRadius.setObjectName(u"graphicsView_CalculatedTipRadius_tabTipRadius")
        sizePolicy1.setHeightForWidth(self.graphicsView_CalculatedTipRadius_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.graphicsView_CalculatedTipRadius_tabTipRadius.setSizePolicy(sizePolicy1)

        self.gridLayout_66.addWidget(self.graphicsView_CalculatedTipRadius_tabTipRadius, 1, 0, 2, 10)

        self.lineEdit_TipRadius_errorBar_tabTipRadius = QLineEdit(self.tab_33)
        self.lineEdit_TipRadius_errorBar_tabTipRadius.setObjectName(u"lineEdit_TipRadius_errorBar_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.lineEdit_TipRadius_errorBar_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_TipRadius_errorBar_tabTipRadius.setSizePolicy(sizePolicy8)

        self.gridLayout_66.addWidget(self.lineEdit_TipRadius_errorBar_tabTipRadius, 0, 3, 1, 1)

        self.graphicsView_tab_TipAreaFunction_5.addTab(self.tab_33, "")

        self.gridLayout_65.addWidget(self.graphicsView_tab_TipAreaFunction_5, 5, 1, 1, 9)

        self.groupBox_4 = QGroupBox(self.tab_8)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy3.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy3)
        self.gridLayout_57 = QGridLayout(self.groupBox_4)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.label_37 = QLabel(self.groupBox_4)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_57.addWidget(self.label_37, 2, 1, 1, 1)

        self.comboBox_Equipment_tabTipRadius = QComboBox(self.groupBox_4)
        self.comboBox_Equipment_tabTipRadius.addItem("")
        self.comboBox_Equipment_tabTipRadius.setObjectName(u"comboBox_Equipment_tabTipRadius")
        self.comboBox_Equipment_tabTipRadius.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBox_Equipment_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.comboBox_Equipment_tabTipRadius.setSizePolicy(sizePolicy)

        self.gridLayout_57.addWidget(self.comboBox_Equipment_tabTipRadius, 2, 2, 1, 1)

        self.label_72 = QLabel(self.groupBox_4)
        self.label_72.setObjectName(u"label_72")
        sizePolicy4.setHeightForWidth(self.label_72.sizePolicy().hasHeightForWidth())
        self.label_72.setSizePolicy(sizePolicy4)
        self.label_72.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_57.addWidget(self.label_72, 1, 1, 1, 1)

        self.comboBox_method_tabTipRadius = QComboBox(self.groupBox_4)
        self.comboBox_method_tabTipRadius.addItem("")
        self.comboBox_method_tabTipRadius.addItem("")
        self.comboBox_method_tabTipRadius.addItem("")
        self.comboBox_method_tabTipRadius.setObjectName(u"comboBox_method_tabTipRadius")
        self.comboBox_method_tabTipRadius.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.comboBox_method_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.comboBox_method_tabTipRadius.setSizePolicy(sizePolicy5)
        self.comboBox_method_tabTipRadius.setMinimumSize(QSize(120, 0))
        self.comboBox_method_tabTipRadius.setEditable(False)

        self.gridLayout_57.addWidget(self.comboBox_method_tabTipRadius, 1, 2, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_4, 2, 1, 1, 1)

        self.groupBox_15 = QGroupBox(self.tab_8)
        self.groupBox_15.setObjectName(u"groupBox_15")
        sizePolicy.setHeightForWidth(self.groupBox_15.sizePolicy().hasHeightForWidth())
        self.groupBox_15.setSizePolicy(sizePolicy)
        self.gridLayout_30 = QGridLayout(self.groupBox_15)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.label_76 = QLabel(self.groupBox_15)
        self.label_76.setObjectName(u"label_76")
        sizePolicy.setHeightForWidth(self.label_76.sizePolicy().hasHeightForWidth())
        self.label_76.setSizePolicy(sizePolicy)

        self.gridLayout_30.addWidget(self.label_76, 0, 5, 1, 1)

        self.label_77 = QLabel(self.groupBox_15)
        self.label_77.setObjectName(u"label_77")
        sizePolicy.setHeightForWidth(self.label_77.sizePolicy().hasHeightForWidth())
        self.label_77.setSizePolicy(sizePolicy)
        self.label_77.setMinimumSize(QSize(110, 0))

        self.gridLayout_30.addWidget(self.label_77, 0, 1, 1, 1)

        self.doubleSpinBox_End_Pmax_tabTipRadius = QDoubleSpinBox(self.groupBox_15)
        self.doubleSpinBox_End_Pmax_tabTipRadius.setObjectName(u"doubleSpinBox_End_Pmax_tabTipRadius")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_End_Pmax_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_End_Pmax_tabTipRadius.setSizePolicy(sizePolicy)
        self.doubleSpinBox_End_Pmax_tabTipRadius.setValue(0.500000000000000)

        self.gridLayout_30.addWidget(self.doubleSpinBox_End_Pmax_tabTipRadius, 0, 6, 1, 1)

        self.label_78 = QLabel(self.groupBox_15)
        self.label_78.setObjectName(u"label_78")
        sizePolicy.setHeightForWidth(self.label_78.sizePolicy().hasHeightForWidth())
        self.label_78.setSizePolicy(sizePolicy)

        self.gridLayout_30.addWidget(self.label_78, 1, 5, 1, 1)

        self.doubleSpinBox_zeroGradDelta_tabTipRadius = QDoubleSpinBox(self.groupBox_15)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius.setObjectName(u"doubleSpinBox_zeroGradDelta_tabTipRadius")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zeroGradDelta_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zeroGradDelta_tabTipRadius.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius.setDecimals(4)
        self.doubleSpinBox_zeroGradDelta_tabTipRadius.setValue(0.010000000000000)

        self.gridLayout_30.addWidget(self.doubleSpinBox_zeroGradDelta_tabTipRadius, 1, 4, 1, 1)

        self.doubleSpinBox_Start_Pmax_tabTipRadius = QDoubleSpinBox(self.groupBox_15)
        self.doubleSpinBox_Start_Pmax_tabTipRadius.setObjectName(u"doubleSpinBox_Start_Pmax_tabTipRadius")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Start_Pmax_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Start_Pmax_tabTipRadius.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Start_Pmax_tabTipRadius.setValue(1.000000000000000)

        self.gridLayout_30.addWidget(self.doubleSpinBox_Start_Pmax_tabTipRadius, 0, 4, 1, 1)

        self.label_79 = QLabel(self.groupBox_15)
        self.label_79.setObjectName(u"label_79")
        sizePolicy.setHeightForWidth(self.label_79.sizePolicy().hasHeightForWidth())
        self.label_79.setSizePolicy(sizePolicy)

        self.gridLayout_30.addWidget(self.label_79, 1, 1, 1, 1)

        self.spinBox_min_size_fluctuation_tabTipRadius = QSpinBox(self.groupBox_15)
        self.spinBox_min_size_fluctuation_tabTipRadius.setObjectName(u"spinBox_min_size_fluctuation_tabTipRadius")
        sizePolicy.setHeightForWidth(self.spinBox_min_size_fluctuation_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.spinBox_min_size_fluctuation_tabTipRadius.setSizePolicy(sizePolicy)
        self.spinBox_min_size_fluctuation_tabTipRadius.setValue(1)

        self.gridLayout_30.addWidget(self.spinBox_min_size_fluctuation_tabTipRadius, 1, 6, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_15, 2, 3, 1, 1)

        self.label_82 = QLabel(self.tab_8)
        self.label_82.setObjectName(u"label_82")
        sizePolicy3.setHeightForWidth(self.label_82.sizePolicy().hasHeightForWidth())
        self.label_82.setSizePolicy(sizePolicy3)

        self.gridLayout_65.addWidget(self.label_82, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_8)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy2.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy2)
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)

        self.gridLayout_65.addWidget(self.frame_9, 2, 4, 1, 6)

        self.groupBox_17 = QGroupBox(self.tab_8)
        self.groupBox_17.setObjectName(u"groupBox_17")
        sizePolicy.setHeightForWidth(self.groupBox_17.sizePolicy().hasHeightForWidth())
        self.groupBox_17.setSizePolicy(sizePolicy)
        self.gridLayout_36 = QGridLayout(self.groupBox_17)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.lineEdit_TipName_tabTipRadius = QLineEdit(self.groupBox_17)
        self.lineEdit_TipName_tabTipRadius.setObjectName(u"lineEdit_TipName_tabTipRadius")
        sizePolicy6.setHeightForWidth(self.lineEdit_TipName_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.lineEdit_TipName_tabTipRadius.setSizePolicy(sizePolicy6)

        self.gridLayout_36.addWidget(self.lineEdit_TipName_tabTipRadius, 0, 1, 1, 1)

        self.label_38 = QLabel(self.groupBox_17)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_36.addWidget(self.label_38, 0, 2, 1, 1)

        self.doubleSpinBox_Poisson_Tip_tabTipRadius = QDoubleSpinBox(self.groupBox_17)
        self.doubleSpinBox_Poisson_Tip_tabTipRadius.setObjectName(u"doubleSpinBox_Poisson_Tip_tabTipRadius")
        self.doubleSpinBox_Poisson_Tip_tabTipRadius.setDecimals(3)
        self.doubleSpinBox_Poisson_Tip_tabTipRadius.setValue(0.070000000000000)

        self.gridLayout_36.addWidget(self.doubleSpinBox_Poisson_Tip_tabTipRadius, 0, 5, 1, 1)

        self.label_71 = QLabel(self.groupBox_17)
        self.label_71.setObjectName(u"label_71")

        self.gridLayout_36.addWidget(self.label_71, 0, 4, 1, 1)

        self.doubleSpinBox_E_Tip_tabTipRadius = QDoubleSpinBox(self.groupBox_17)
        self.doubleSpinBox_E_Tip_tabTipRadius.setObjectName(u"doubleSpinBox_E_Tip_tabTipRadius")
        self.doubleSpinBox_E_Tip_tabTipRadius.setDecimals(3)
        self.doubleSpinBox_E_Tip_tabTipRadius.setMaximum(99999.990000000005239)
        self.doubleSpinBox_E_Tip_tabTipRadius.setValue(1141.000000000000000)

        self.gridLayout_36.addWidget(self.doubleSpinBox_E_Tip_tabTipRadius, 0, 3, 1, 1)

        self.label_70 = QLabel(self.groupBox_17)
        self.label_70.setObjectName(u"label_70")

        self.gridLayout_36.addWidget(self.label_70, 0, 0, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_17, 1, 0, 1, 11)

        self.pushButton_Calculate_tabTipRadius = QPushButton(self.tab_8)
        self.pushButton_Calculate_tabTipRadius.setObjectName(u"pushButton_Calculate_tabTipRadius")
        sizePolicy8.setHeightForWidth(self.pushButton_Calculate_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.pushButton_Calculate_tabTipRadius.setSizePolicy(sizePolicy8)

        self.gridLayout_65.addWidget(self.pushButton_Calculate_tabTipRadius, 3, 1, 1, 1)

        self.groupBox_28 = QGroupBox(self.tab_8)
        self.groupBox_28.setObjectName(u"groupBox_28")
        sizePolicy3.setHeightForWidth(self.groupBox_28.sizePolicy().hasHeightForWidth())
        self.groupBox_28.setSizePolicy(sizePolicy3)
        self.groupBox_28.setMinimumSize(QSize(200, 0))
        self.gridLayout_59 = QGridLayout(self.groupBox_28)
        self.gridLayout_59.setObjectName(u"gridLayout_59")
        self.lineEdit_FrameCompliance_tabTipRadius = QLineEdit(self.groupBox_28)
        self.lineEdit_FrameCompliance_tabTipRadius.setObjectName(u"lineEdit_FrameCompliance_tabTipRadius")
        self.lineEdit_FrameCompliance_tabTipRadius.setReadOnly(True)

        self.gridLayout_59.addWidget(self.lineEdit_FrameCompliance_tabTipRadius, 0, 0, 1, 1)

        self.Copy_FrameCompliance_tabTipRadius = QPushButton(self.groupBox_28)
        self.Copy_FrameCompliance_tabTipRadius.setObjectName(u"Copy_FrameCompliance_tabTipRadius")

        self.gridLayout_59.addWidget(self.Copy_FrameCompliance_tabTipRadius, 1, 0, 1, 1)


        self.gridLayout_65.addWidget(self.groupBox_28, 2, 0, 1, 1)

        self.tableWidget_tabTipRadius = QTableWidget(self.tab_8)
        if (self.tableWidget_tabTipRadius.columnCount() < 4):
            self.tableWidget_tabTipRadius.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTipRadius.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTipRadius.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabTipRadius.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        if (self.tableWidget_tabTipRadius.rowCount() < 1):
            self.tableWidget_tabTipRadius.setRowCount(1)
        self.tableWidget_tabTipRadius.setObjectName(u"tableWidget_tabTipRadius")
        sizePolicy10.setHeightForWidth(self.tableWidget_tabTipRadius.sizePolicy().hasHeightForWidth())
        self.tableWidget_tabTipRadius.setSizePolicy(sizePolicy10)
        self.tableWidget_tabTipRadius.setMinimumSize(QSize(200, 0))
        self.tableWidget_tabTipRadius.setMaximumSize(QSize(200, 16777215))
        self.tableWidget_tabTipRadius.setAutoScroll(True)
        self.tableWidget_tabTipRadius.setRowCount(1)
        self.tableWidget_tabTipRadius.setColumnCount(4)
        self.tableWidget_tabTipRadius.horizontalHeader().setVisible(True)
        self.tableWidget_tabTipRadius.horizontalHeader().setMinimumSectionSize(65)
        self.tableWidget_tabTipRadius.horizontalHeader().setDefaultSectionSize(65)
        self.tableWidget_tabTipRadius.horizontalHeader().setHighlightSections(True)
        self.tableWidget_tabTipRadius.horizontalHeader().setProperty("showSortIndicator", True)

        self.gridLayout_65.addWidget(self.tableWidget_tabTipRadius, 5, 0, 3, 1)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.graphicsView_tab_TipAreaFunction_5.raise_()
        self.groupBox_17.raise_()
        self.groupBox_29.raise_()
        self.tableWidget_tabTipRadius.raise_()
        self.pushButton_Calculate_tabTipRadius.raise_()
        self.groupBox_28.raise_()
        self.groupBox_4.raise_()
        self.label_82.raise_()
        self.groupBox_27.raise_()
        self.groupBox_15.raise_()
        self.frame_9.raise_()

        self.gridLayout_16.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.gridLayout_27 = QGridLayout(self.tab_13)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.tabWidget_5 = QTabWidget(self.tab_13)
        self.tabWidget_5.setObjectName(u"tabWidget_5")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.gridLayout_37 = QGridLayout(self.tab_14)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.groupBox_26 = QGroupBox(self.tab_14)
        self.groupBox_26.setObjectName(u"groupBox_26")
        sizePolicy3.setHeightForWidth(self.groupBox_26.sizePolicy().hasHeightForWidth())
        self.groupBox_26.setSizePolicy(sizePolicy3)
        self.gridLayout_56 = QGridLayout(self.groupBox_26)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_26)
        self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness.setValue(0.100000000000000)

        self.gridLayout_56.addWidget(self.doubleSpinBox_critDepthStiffness_tabHE_FrameStiffness, 0, 1, 1, 1)

        self.label_68 = QLabel(self.groupBox_26)
        self.label_68.setObjectName(u"label_68")
        sizePolicy3.setHeightForWidth(self.label_68.sizePolicy().hasHeightForWidth())
        self.label_68.setSizePolicy(sizePolicy3)

        self.gridLayout_56.addWidget(self.label_68, 0, 0, 1, 1)

        self.label_69 = QLabel(self.groupBox_26)
        self.label_69.setObjectName(u"label_69")
        sizePolicy3.setHeightForWidth(self.label_69.sizePolicy().hasHeightForWidth())
        self.label_69.setSizePolicy(sizePolicy3)

        self.gridLayout_56.addWidget(self.label_69, 1, 0, 1, 1)

        self.doubleSpinBox_critForceStiffness_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_26)
        self.doubleSpinBox_critForceStiffness_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_critForceStiffness_tabHE_FrameStiffness")
        self.doubleSpinBox_critForceStiffness_tabHE_FrameStiffness.setValue(10.000000000000000)

        self.gridLayout_56.addWidget(self.doubleSpinBox_critForceStiffness_tabHE_FrameStiffness, 1, 1, 1, 1)


        self.gridLayout_37.addWidget(self.groupBox_26, 2, 3, 1, 1)

        self.label_45 = QLabel(self.tab_14)
        self.label_45.setObjectName(u"label_45")
        sizePolicy3.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy3)

        self.gridLayout_37.addWidget(self.label_45, 4, 0, 1, 1)

        self.groupBox_16 = QGroupBox(self.tab_14)
        self.groupBox_16.setObjectName(u"groupBox_16")
        sizePolicy.setHeightForWidth(self.groupBox_16.sizePolicy().hasHeightForWidth())
        self.groupBox_16.setSizePolicy(sizePolicy)
        self.gridLayout_35 = QGridLayout(self.groupBox_16)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_16)
        self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_End_Pmax_tabHE_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness.setValue(0.500000000000000)

        self.gridLayout_35.addWidget(self.doubleSpinBox_End_Pmax_tabHE_FrameStiffness, 0, 5, 1, 1)

        self.label_41 = QLabel(self.groupBox_16)
        self.label_41.setObjectName(u"label_41")
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)

        self.gridLayout_35.addWidget(self.label_41, 0, 0, 1, 1)

        self.label_42 = QLabel(self.groupBox_16)
        self.label_42.setObjectName(u"label_42")
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)

        self.gridLayout_35.addWidget(self.label_42, 1, 4, 1, 1)

        self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_16)
        self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness.setDecimals(4)
        self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness.setValue(0.010000000000000)

        self.gridLayout_35.addWidget(self.doubleSpinBox_zeroGradDelta_tabHE_FrameStiffness, 1, 3, 1, 1)

        self.label_43 = QLabel(self.groupBox_16)
        self.label_43.setObjectName(u"label_43")
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)

        self.gridLayout_35.addWidget(self.label_43, 1, 0, 1, 1)

        self.spinBox_min_size_fluctuation_tabHE_FrameStiffness = QSpinBox(self.groupBox_16)
        self.spinBox_min_size_fluctuation_tabHE_FrameStiffness.setObjectName(u"spinBox_min_size_fluctuation_tabHE_FrameStiffness")
        sizePolicy.setHeightForWidth(self.spinBox_min_size_fluctuation_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.spinBox_min_size_fluctuation_tabHE_FrameStiffness.setSizePolicy(sizePolicy)
        self.spinBox_min_size_fluctuation_tabHE_FrameStiffness.setValue(1)

        self.gridLayout_35.addWidget(self.spinBox_min_size_fluctuation_tabHE_FrameStiffness, 1, 5, 1, 1)

        self.label_44 = QLabel(self.groupBox_16)
        self.label_44.setObjectName(u"label_44")
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)

        self.gridLayout_35.addWidget(self.label_44, 0, 4, 1, 1)

        self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_16)
        self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_Start_Pmax_tabHE_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness.setValue(1.000000000000000)

        self.gridLayout_35.addWidget(self.doubleSpinBox_Start_Pmax_tabHE_FrameStiffness, 0, 3, 1, 1)


        self.gridLayout_37.addWidget(self.groupBox_16, 2, 2, 1, 1)

        self.tableWidget_tabHE_FrameStiffness = QTableWidget(self.tab_14)
        if (self.tableWidget_tabHE_FrameStiffness.columnCount() < 2):
            self.tableWidget_tabHE_FrameStiffness.setColumnCount(2)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabHE_FrameStiffness.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabHE_FrameStiffness.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        if (self.tableWidget_tabHE_FrameStiffness.rowCount() < 1):
            self.tableWidget_tabHE_FrameStiffness.setRowCount(1)
        self.tableWidget_tabHE_FrameStiffness.setObjectName(u"tableWidget_tabHE_FrameStiffness")
        sizePolicy1.setHeightForWidth(self.tableWidget_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.tableWidget_tabHE_FrameStiffness.setSizePolicy(sizePolicy1)
        self.tableWidget_tabHE_FrameStiffness.setMinimumSize(QSize(200, 0))
        self.tableWidget_tabHE_FrameStiffness.setMaximumSize(QSize(200, 16777215))
        self.tableWidget_tabHE_FrameStiffness.setAutoScroll(True)
        self.tableWidget_tabHE_FrameStiffness.setRowCount(1)
        self.tableWidget_tabHE_FrameStiffness.horizontalHeader().setVisible(True)
        self.tableWidget_tabHE_FrameStiffness.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget_tabHE_FrameStiffness.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_tabHE_FrameStiffness.horizontalHeader().setHighlightSections(True)
        self.tableWidget_tabHE_FrameStiffness.horizontalHeader().setProperty("showSortIndicator", True)

        self.gridLayout_37.addWidget(self.tableWidget_tabHE_FrameStiffness, 5, 0, 1, 1)

        self.groupBox_25 = QGroupBox(self.tab_14)
        self.groupBox_25.setObjectName(u"groupBox_25")
        sizePolicy3.setHeightForWidth(self.groupBox_25.sizePolicy().hasHeightForWidth())
        self.groupBox_25.setSizePolicy(sizePolicy3)
        self.groupBox_25.setMinimumSize(QSize(253, 0))
        self.groupBox_25.setMaximumSize(QSize(253, 16777215))
        self.gridLayout_55 = QGridLayout(self.groupBox_25)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness = QCheckBox(self.groupBox_25)
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setObjectName(u"checkBox_UsingRate2findSurface_tabHE_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setMinimumSize(QSize(0, 0))
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setChecked(True)

        self.gridLayout_55.addWidget(self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness, 0, 0, 1, 1)

        self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness = QDoubleSpinBox(self.groupBox_25)
        self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness.setObjectName(u"doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness.setDecimals(1)
        self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness.setValue(1.000000000000000)

        self.gridLayout_55.addWidget(self.doubleSpinBox_Rate2findSurface_tabHE_FrameStiffness, 0, 1, 1, 1)


        self.gridLayout_37.addWidget(self.groupBox_25, 2, 1, 1, 1)

        self.groupBox_14 = QGroupBox(self.tab_14)
        self.groupBox_14.setObjectName(u"groupBox_14")
        sizePolicy.setHeightForWidth(self.groupBox_14.sizePolicy().hasHeightForWidth())
        self.groupBox_14.setSizePolicy(sizePolicy)
        self.gridLayout_29 = QGridLayout(self.groupBox_14)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.label_35 = QLabel(self.groupBox_14)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_29.addWidget(self.label_35, 2, 1, 1, 1)

        self.comboBox_Equipment_tabHE_FrameStiffness = QComboBox(self.groupBox_14)
        self.comboBox_Equipment_tabHE_FrameStiffness.addItem("")
        self.comboBox_Equipment_tabHE_FrameStiffness.setObjectName(u"comboBox_Equipment_tabHE_FrameStiffness")
        self.comboBox_Equipment_tabHE_FrameStiffness.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.comboBox_Equipment_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.comboBox_Equipment_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)

        self.gridLayout_29.addWidget(self.comboBox_Equipment_tabHE_FrameStiffness, 2, 2, 1, 1)

        self.label_36 = QLabel(self.groupBox_14)
        self.label_36.setObjectName(u"label_36")
        sizePolicy4.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy4)
        self.label_36.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_29.addWidget(self.label_36, 1, 1, 1, 1)

        self.comboBox_method_tabHE_FrameStiffness = QComboBox(self.groupBox_14)
        self.comboBox_method_tabHE_FrameStiffness.addItem("")
        self.comboBox_method_tabHE_FrameStiffness.addItem("")
        self.comboBox_method_tabHE_FrameStiffness.addItem("")
        self.comboBox_method_tabHE_FrameStiffness.setObjectName(u"comboBox_method_tabHE_FrameStiffness")
        self.comboBox_method_tabHE_FrameStiffness.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.comboBox_method_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.comboBox_method_tabHE_FrameStiffness.setSizePolicy(sizePolicy5)
        self.comboBox_method_tabHE_FrameStiffness.setMinimumSize(QSize(120, 0))
        self.comboBox_method_tabHE_FrameStiffness.setEditable(False)

        self.gridLayout_29.addWidget(self.comboBox_method_tabHE_FrameStiffness, 1, 2, 1, 1)


        self.gridLayout_37.addWidget(self.groupBox_14, 2, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.tab_14)
        self.groupBox_13.setObjectName(u"groupBox_13")
        sizePolicy7.setHeightForWidth(self.groupBox_13.sizePolicy().hasHeightForWidth())
        self.groupBox_13.setSizePolicy(sizePolicy7)
        self.gridLayout_28 = QGridLayout(self.groupBox_13)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.lineEdit_path_tabHE_FrameStiffness = QLineEdit(self.groupBox_13)
        self.lineEdit_path_tabHE_FrameStiffness.setObjectName(u"lineEdit_path_tabHE_FrameStiffness")
        sizePolicy17.setHeightForWidth(self.lineEdit_path_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_path_tabHE_FrameStiffness.setSizePolicy(sizePolicy17)

        self.gridLayout_28.addWidget(self.lineEdit_path_tabHE_FrameStiffness, 0, 1, 1, 1)


        self.gridLayout_37.addWidget(self.groupBox_13, 0, 0, 1, 6)

        self.graphicsView_tab_TipAreaFunction_3 = QTabWidget(self.tab_14)
        self.graphicsView_tab_TipAreaFunction_3.setObjectName(u"graphicsView_tab_TipAreaFunction_3")
        sizePolicy16.setHeightForWidth(self.graphicsView_tab_TipAreaFunction_3.sizePolicy().hasHeightForWidth())
        self.graphicsView_tab_TipAreaFunction_3.setSizePolicy(sizePolicy16)
        self.graphicsView_tab_TipAreaFunction_3.setUsesScrollButtons(True)
        self.tab_16 = QWidget()
        self.tab_16.setObjectName(u"tab_16")
        self.gridLayout_31 = QGridLayout(self.tab_16)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.tabWidget_6 = QTabWidget(self.tab_16)
        self.tabWidget_6.setObjectName(u"tabWidget_6")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.gridLayout_32 = QGridLayout(self.tab_17)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness = QPushButton(self.tab_17)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness")
        sizePolicy7.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setSizePolicy(sizePolicy7)

        self.gridLayout_32.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness, 2, 1, 1, 1)

        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness = QGraphicsView(self.tab_17)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setObjectName(u"graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness")
        sizePolicy14.setHeightForWidth(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setSizePolicy(sizePolicy14)

        self.gridLayout_32.addWidget(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE_FrameStiffness, 1, 0, 1, 4)

        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE_FrameStiffness = QCheckBox(self.tab_17)
        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE_FrameStiffness.setObjectName(u"checkBox_iLHU_inclusive_frame_stiffness_tabHE_FrameStiffness")

        self.gridLayout_32.addWidget(self.checkBox_iLHU_inclusive_frame_stiffness_tabHE_FrameStiffness, 2, 3, 1, 1)

        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE_FrameStiffness = QCheckBox(self.tab_17)
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setObjectName(u"checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE_FrameStiffness")

        self.gridLayout_32.addWidget(self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE_FrameStiffness, 2, 2, 1, 1)

        self.tabWidget_6.addTab(self.tab_17, "")
        self.tab_18 = QWidget()
        self.tab_18.setObjectName(u"tab_18")
        self.gridLayout_33 = QGridLayout(self.tab_18)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_3 = QGraphicsView(self.tab_18)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_3.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_3")
        sizePolicy1.setHeightForWidth(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_3.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_3.setSizePolicy(sizePolicy1)

        self.gridLayout_33.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_3, 0, 0, 1, 1)

        self.tabWidget_6.addTab(self.tab_18, "")

        self.gridLayout_31.addWidget(self.tabWidget_6, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_3.addTab(self.tab_16, "")
        self.tab_19 = QWidget()
        self.tab_19.setObjectName(u"tab_19")
        self.gridLayout_34 = QGridLayout(self.tab_19)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.label_40 = QLabel(self.tab_19)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_34.addWidget(self.label_40, 1, 0, 1, 1)

        self.lineEdit_FrameStiffness_tabHE_FrameStiffness = QLineEdit(self.tab_19)
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setObjectName(u"lineEdit_FrameStiffness_tabHE_FrameStiffness")
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setEnabled(True)
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameStiffness_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setFrame(True)
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setDragEnabled(False)
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setReadOnly(True)
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setClearButtonEnabled(False)

        self.gridLayout_34.addWidget(self.lineEdit_FrameStiffness_tabHE_FrameStiffness, 1, 1, 1, 1)

        self.label_39 = QLabel(self.tab_19)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_34.addWidget(self.label_39, 1, 2, 1, 1)

        self.graphicsView_tabHE_FrameStiffness = QGraphicsView(self.tab_19)
        self.graphicsView_tabHE_FrameStiffness.setObjectName(u"graphicsView_tabHE_FrameStiffness")
        self.graphicsView_tabHE_FrameStiffness.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_34.addWidget(self.graphicsView_tabHE_FrameStiffness, 3, 0, 1, 7)

        self.lineEdit_FrameCompliance_tabHE_FrameStiffness = QLineEdit(self.tab_19)
        self.lineEdit_FrameCompliance_tabHE_FrameStiffness.setObjectName(u"lineEdit_FrameCompliance_tabHE_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.lineEdit_FrameCompliance_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.lineEdit_FrameCompliance_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)
        self.lineEdit_FrameCompliance_tabHE_FrameStiffness.setReadOnly(True)

        self.gridLayout_34.addWidget(self.lineEdit_FrameCompliance_tabHE_FrameStiffness, 1, 3, 1, 1)

        self.graphicsView_tab_TipAreaFunction_3.addTab(self.tab_19, "")

        self.gridLayout_37.addWidget(self.graphicsView_tab_TipAreaFunction_3, 5, 1, 1, 5)

        self.pushButton_Calculate_tabHE_FrameStiffness = QPushButton(self.tab_14)
        self.pushButton_Calculate_tabHE_FrameStiffness.setObjectName(u"pushButton_Calculate_tabHE_FrameStiffness")
        sizePolicy8.setHeightForWidth(self.pushButton_Calculate_tabHE_FrameStiffness.sizePolicy().hasHeightForWidth())
        self.pushButton_Calculate_tabHE_FrameStiffness.setSizePolicy(sizePolicy8)

        self.gridLayout_37.addWidget(self.pushButton_Calculate_tabHE_FrameStiffness, 4, 1, 1, 1)

        self.frame_3 = QFrame(self.tab_14)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy18 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy18.setHorizontalStretch(0)
        sizePolicy18.setVerticalStretch(0)
        sizePolicy18.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy18)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout_37.addWidget(self.frame_3, 2, 4, 1, 2)

        self.progressBar_tabHE_FrameStiffness = QProgressBar(self.tab_14)
        self.progressBar_tabHE_FrameStiffness.setObjectName(u"progressBar_tabHE_FrameStiffness")
        self.progressBar_tabHE_FrameStiffness.setValue(0)

        self.gridLayout_37.addWidget(self.progressBar_tabHE_FrameStiffness, 4, 2, 1, 2)

        self.tabWidget_5.addTab(self.tab_14, "")
        self.tab_15 = QWidget()
        self.tab_15.setObjectName(u"tab_15")
        self.gridLayout_48 = QGridLayout(self.tab_15)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.groupBox_23 = QGroupBox(self.tab_15)
        self.groupBox_23.setObjectName(u"groupBox_23")
        sizePolicy9.setHeightForWidth(self.groupBox_23.sizePolicy().hasHeightForWidth())
        self.groupBox_23.setSizePolicy(sizePolicy9)
        self.groupBox_23.setMinimumSize(QSize(800, 0))
        self.gridLayout_43 = QGridLayout(self.groupBox_23)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.label_58 = QLabel(self.groupBox_23)
        self.label_58.setObjectName(u"label_58")
        sizePolicy3.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_58, 1, 11, 1, 1)

        self.lineEdit_TAF4_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TAF4_tabHE.setObjectName(u"lineEdit_TAF4_tabHE")
        self.lineEdit_TAF4_tabHE.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_TAF4_tabHE, 1, 8, 1, 1)

        self.lineEdit_TAF3_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TAF3_tabHE.setObjectName(u"lineEdit_TAF3_tabHE")
        self.lineEdit_TAF3_tabHE.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_TAF3_tabHE, 1, 6, 1, 1)

        self.label_56 = QLabel(self.groupBox_23)
        self.label_56.setObjectName(u"label_56")
        sizePolicy3.setHeightForWidth(self.label_56.sizePolicy().hasHeightForWidth())
        self.label_56.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_56, 1, 1, 1, 1)

        self.lineEdit_TAF1_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TAF1_tabHE.setObjectName(u"lineEdit_TAF1_tabHE")
        self.lineEdit_TAF1_tabHE.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_TAF1_tabHE, 1, 2, 1, 1)

        self.lineEdit_TAF2_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TAF2_tabHE.setObjectName(u"lineEdit_TAF2_tabHE")
        self.lineEdit_TAF2_tabHE.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_TAF2_tabHE, 1, 4, 1, 1)

        self.label_57 = QLabel(self.groupBox_23)
        self.label_57.setObjectName(u"label_57")
        sizePolicy3.setHeightForWidth(self.label_57.sizePolicy().hasHeightForWidth())
        self.label_57.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_57, 1, 3, 1, 1)

        self.label_55 = QLabel(self.groupBox_23)
        self.label_55.setObjectName(u"label_55")
        sizePolicy3.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_55, 1, 5, 1, 1)

        self.label_54 = QLabel(self.groupBox_23)
        self.label_54.setObjectName(u"label_54")
        sizePolicy3.setHeightForWidth(self.label_54.sizePolicy().hasHeightForWidth())
        self.label_54.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_54, 1, 7, 1, 1)

        self.lineEdit_TAF5_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TAF5_tabHE.setObjectName(u"lineEdit_TAF5_tabHE")
        self.lineEdit_TAF5_tabHE.setReadOnly(True)

        self.gridLayout_43.addWidget(self.lineEdit_TAF5_tabHE, 1, 10, 1, 1)

        self.label_53 = QLabel(self.groupBox_23)
        self.label_53.setObjectName(u"label_53")
        sizePolicy3.setHeightForWidth(self.label_53.sizePolicy().hasHeightForWidth())
        self.label_53.setSizePolicy(sizePolicy3)

        self.gridLayout_43.addWidget(self.label_53, 1, 9, 1, 1)

        self.label_60 = QLabel(self.groupBox_23)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_43.addWidget(self.label_60, 1, 0, 1, 1)

        self.label_52 = QLabel(self.groupBox_23)
        self.label_52.setObjectName(u"label_52")
        sizePolicy11.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy11)
        self.label_52.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_43.addWidget(self.label_52, 0, 0, 1, 1)

        self.label_62 = QLabel(self.groupBox_23)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setScaledContents(True)
        self.label_62.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_43.addWidget(self.label_62, 0, 8, 1, 1)

        self.Copy_TAF_tabHE = QPushButton(self.groupBox_23)
        self.Copy_TAF_tabHE.setObjectName(u"Copy_TAF_tabHE")
        sizePolicy19 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.Copy_TAF_tabHE.sizePolicy().hasHeightForWidth())
        self.Copy_TAF_tabHE.setSizePolicy(sizePolicy19)

        self.gridLayout_43.addWidget(self.Copy_TAF_tabHE, 0, 13, 2, 1)

        self.label_61 = QLabel(self.groupBox_23)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_43.addWidget(self.label_61, 0, 4, 1, 2)

        self.lineEdit_TipName_tabHE = QLineEdit(self.groupBox_23)
        self.lineEdit_TipName_tabHE.setObjectName(u"lineEdit_TipName_tabHE")

        self.gridLayout_43.addWidget(self.lineEdit_TipName_tabHE, 0, 1, 1, 3)

        self.doubleSpinBox_E_Tip_tabHE = QDoubleSpinBox(self.groupBox_23)
        self.doubleSpinBox_E_Tip_tabHE.setObjectName(u"doubleSpinBox_E_Tip_tabHE")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_E_Tip_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_E_Tip_tabHE.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_E_Tip_tabHE.setDecimals(3)
        self.doubleSpinBox_E_Tip_tabHE.setMaximum(99999.990000000005239)
        self.doubleSpinBox_E_Tip_tabHE.setValue(1141.000000000000000)

        self.gridLayout_43.addWidget(self.doubleSpinBox_E_Tip_tabHE, 0, 6, 1, 1)

        self.doubleSpinBox_Poisson_Tip_tabHE = QDoubleSpinBox(self.groupBox_23)
        self.doubleSpinBox_Poisson_Tip_tabHE.setObjectName(u"doubleSpinBox_Poisson_Tip_tabHE")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_Poisson_Tip_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Poisson_Tip_tabHE.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_Poisson_Tip_tabHE.setDecimals(3)
        self.doubleSpinBox_Poisson_Tip_tabHE.setValue(0.070000000000000)

        self.gridLayout_43.addWidget(self.doubleSpinBox_Poisson_Tip_tabHE, 0, 10, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_23, 1, 0, 1, 4)

        self.progressBar_tabHE = QProgressBar(self.tab_15)
        self.progressBar_tabHE.setObjectName(u"progressBar_tabHE")
        self.progressBar_tabHE.setValue(0)

        self.gridLayout_48.addWidget(self.progressBar_tabHE, 4, 2, 1, 3)

        self.groupBox_21 = QGroupBox(self.tab_15)
        self.groupBox_21.setObjectName(u"groupBox_21")
        sizePolicy3.setHeightForWidth(self.groupBox_21.sizePolicy().hasHeightForWidth())
        self.groupBox_21.setSizePolicy(sizePolicy3)
        self.groupBox_21.setMinimumSize(QSize(0, 0))
        self.gridLayout_41 = QGridLayout(self.groupBox_21)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.checkBox_UsingRate2findSurface_tabHE = QCheckBox(self.groupBox_21)
        self.checkBox_UsingRate2findSurface_tabHE.setObjectName(u"checkBox_UsingRate2findSurface_tabHE")
        sizePolicy8.setHeightForWidth(self.checkBox_UsingRate2findSurface_tabHE.sizePolicy().hasHeightForWidth())
        self.checkBox_UsingRate2findSurface_tabHE.setSizePolicy(sizePolicy8)
        self.checkBox_UsingRate2findSurface_tabHE.setChecked(True)

        self.gridLayout_41.addWidget(self.checkBox_UsingRate2findSurface_tabHE, 0, 0, 1, 1)

        self.doubleSpinBox_Rate2findSurface_tabHE = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_Rate2findSurface_tabHE.setObjectName(u"doubleSpinBox_Rate2findSurface_tabHE")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Rate2findSurface_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Rate2findSurface_tabHE.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Rate2findSurface_tabHE.setDecimals(1)
        self.doubleSpinBox_Rate2findSurface_tabHE.setValue(1.000000000000000)

        self.gridLayout_41.addWidget(self.doubleSpinBox_Rate2findSurface_tabHE, 0, 1, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_21, 3, 2, 1, 1)

        self.Calculate_tabHE = QPushButton(self.tab_15)
        self.Calculate_tabHE.setObjectName(u"Calculate_tabHE")

        self.gridLayout_48.addWidget(self.Calculate_tabHE, 4, 1, 1, 1)

        self.groupBox_19 = QGroupBox(self.tab_15)
        self.groupBox_19.setObjectName(u"groupBox_19")
        sizePolicy.setHeightForWidth(self.groupBox_19.sizePolicy().hasHeightForWidth())
        self.groupBox_19.setSizePolicy(sizePolicy)
        self.gridLayout_39 = QGridLayout(self.groupBox_19)
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.label_46 = QLabel(self.groupBox_19)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_39.addWidget(self.label_46, 2, 1, 1, 1)

        self.comboBox_Equipment_tabHE = QComboBox(self.groupBox_19)
        self.comboBox_Equipment_tabHE.addItem("")
        self.comboBox_Equipment_tabHE.setObjectName(u"comboBox_Equipment_tabHE")
        self.comboBox_Equipment_tabHE.setEnabled(False)
        sizePolicy8.setHeightForWidth(self.comboBox_Equipment_tabHE.sizePolicy().hasHeightForWidth())
        self.comboBox_Equipment_tabHE.setSizePolicy(sizePolicy8)

        self.gridLayout_39.addWidget(self.comboBox_Equipment_tabHE, 2, 2, 1, 1)

        self.label_47 = QLabel(self.groupBox_19)
        self.label_47.setObjectName(u"label_47")
        sizePolicy4.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy4)
        self.label_47.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_39.addWidget(self.label_47, 1, 1, 1, 1)

        self.comboBox_method_tabHE = QComboBox(self.groupBox_19)
        self.comboBox_method_tabHE.addItem("")
        self.comboBox_method_tabHE.addItem("")
        self.comboBox_method_tabHE.addItem("")
        self.comboBox_method_tabHE.setObjectName(u"comboBox_method_tabHE")
        self.comboBox_method_tabHE.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.comboBox_method_tabHE.sizePolicy().hasHeightForWidth())
        self.comboBox_method_tabHE.setSizePolicy(sizePolicy5)
        self.comboBox_method_tabHE.setMinimumSize(QSize(120, 0))
        self.comboBox_method_tabHE.setEditable(False)

        self.gridLayout_39.addWidget(self.comboBox_method_tabHE, 1, 2, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_19, 3, 1, 1, 1)

        self.frame_5 = QFrame(self.tab_15)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)

        self.gridLayout_48.addWidget(self.frame_5, 1, 8, 1, 1)

        self.tableWidget_tabHE = QTableWidget(self.tab_15)
        if (self.tableWidget_tabHE.columnCount() < 2):
            self.tableWidget_tabHE.setColumnCount(2)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabHE.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_tabHE.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        if (self.tableWidget_tabHE.rowCount() < 1):
            self.tableWidget_tabHE.setRowCount(1)
        self.tableWidget_tabHE.setObjectName(u"tableWidget_tabHE")
        sizePolicy10.setHeightForWidth(self.tableWidget_tabHE.sizePolicy().hasHeightForWidth())
        self.tableWidget_tabHE.setSizePolicy(sizePolicy10)
        self.tableWidget_tabHE.setMinimumSize(QSize(180, 0))
        self.tableWidget_tabHE.setMaximumSize(QSize(200, 16777215))
        self.tableWidget_tabHE.setAutoScroll(True)
        self.tableWidget_tabHE.setRowCount(1)
        self.tableWidget_tabHE.horizontalHeader().setVisible(True)
        self.tableWidget_tabHE.horizontalHeader().setMinimumSectionSize(80)
        self.tableWidget_tabHE.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_tabHE.horizontalHeader().setHighlightSections(True)
        self.tableWidget_tabHE.horizontalHeader().setProperty("showSortIndicator", True)

        self.gridLayout_48.addWidget(self.tableWidget_tabHE, 5, 0, 3, 1)

        self.label_59 = QLabel(self.tab_15)
        self.label_59.setObjectName(u"label_59")
        sizePolicy3.setHeightForWidth(self.label_59.sizePolicy().hasHeightForWidth())
        self.label_59.setSizePolicy(sizePolicy3)

        self.gridLayout_48.addWidget(self.label_59, 4, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_4 = QTabWidget(self.tab_15)
        self.graphicsView_tab_TipAreaFunction_4.setObjectName(u"graphicsView_tab_TipAreaFunction_4")
        sizePolicy1.setHeightForWidth(self.graphicsView_tab_TipAreaFunction_4.sizePolicy().hasHeightForWidth())
        self.graphicsView_tab_TipAreaFunction_4.setSizePolicy(sizePolicy1)
        self.graphicsView_tab_TipAreaFunction_4.setUsesScrollButtons(True)
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.gridLayout_44 = QGridLayout(self.tab_20)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE = QTabWidget(self.tab_20)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE")
        self.tab_21 = QWidget()
        self.tab_21.setObjectName(u"tab_21")
        self.gridLayout_45 = QGridLayout(self.tab_21)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE = QPushButton(self.tab_21)
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE.setObjectName(u"pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE")
        sizePolicy7.setHeightForWidth(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE.setSizePolicy(sizePolicy7)

        self.gridLayout_45.addWidget(self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE, 3, 1, 1, 1)

        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE = QGraphicsView(self.tab_21)
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE.setObjectName(u"graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE")
        sizePolicy14.setHeightForWidth(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE.setSizePolicy(sizePolicy14)

        self.gridLayout_45.addWidget(self.graphicsView_load_depth_tab_inclusive_frame_stiffness_tabHE, 1, 0, 1, 4)

        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE = QCheckBox(self.tab_21)
        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE.setObjectName(u"checkBox_iLHU_inclusive_frame_stiffness_tabHE")

        self.gridLayout_45.addWidget(self.checkBox_iLHU_inclusive_frame_stiffness_tabHE, 3, 3, 1, 1)

        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE = QCheckBox(self.tab_21)
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE.setObjectName(u"checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE")

        self.gridLayout_45.addWidget(self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE, 3, 2, 1, 1)

        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.addTab(self.tab_21, "")
        self.tab_22 = QWidget()
        self.tab_22.setObjectName(u"tab_22")
        self.gridLayout_46 = QGridLayout(self.tab_22)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_4 = QGraphicsView(self.tab_22)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_4.setObjectName(u"graphicsView_load_depth_tab_exclusive_frame_stiffness_4")
        sizePolicy1.setHeightForWidth(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_4.sizePolicy().hasHeightForWidth())
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_4.setSizePolicy(sizePolicy1)

        self.gridLayout_46.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_4, 0, 0, 1, 1)

        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.addTab(self.tab_22, "")

        self.gridLayout_44.addWidget(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_4.addTab(self.tab_20, "")
        self.tab_23 = QWidget()
        self.tab_23.setObjectName(u"tab_23")
        self.gridLayout_11 = QGridLayout(self.tab_23)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.tabWidget_7 = QTabWidget(self.tab_23)
        self.tabWidget_7.setObjectName(u"tabWidget_7")
        self.tab_25 = QWidget()
        self.tab_25.setObjectName(u"tab_25")
        self.gridLayout_50 = QGridLayout(self.tab_25)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.graphicsView_H_hc_tabHE = QGraphicsView(self.tab_25)
        self.graphicsView_H_hc_tabHE.setObjectName(u"graphicsView_H_hc_tabHE")
        self.graphicsView_H_hc_tabHE.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_50.addWidget(self.graphicsView_H_hc_tabHE, 0, 0, 1, 1)

        self.tabWidget_7.addTab(self.tab_25, "")
        self.tab_26 = QWidget()
        self.tab_26.setObjectName(u"tab_26")
        self.gridLayout_51 = QGridLayout(self.tab_26)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.graphicsView_H_Index_tabHE = QGraphicsView(self.tab_26)
        self.graphicsView_H_Index_tabHE.setObjectName(u"graphicsView_H_Index_tabHE")
        self.graphicsView_H_Index_tabHE.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_51.addWidget(self.graphicsView_H_Index_tabHE, 0, 0, 1, 1)

        self.tabWidget_7.addTab(self.tab_26, "")

        self.gridLayout_11.addWidget(self.tabWidget_7, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_4.addTab(self.tab_23, "")
        self.tab_24 = QWidget()
        self.tab_24.setObjectName(u"tab_24")
        self.gridLayout_47 = QGridLayout(self.tab_24)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.tabWidget_8 = QTabWidget(self.tab_24)
        self.tabWidget_8.setObjectName(u"tabWidget_8")
        self.tab_27 = QWidget()
        self.tab_27.setObjectName(u"tab_27")
        self.gridLayout_53 = QGridLayout(self.tab_27)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.graphicsView_E_hc_tabHE = QGraphicsView(self.tab_27)
        self.graphicsView_E_hc_tabHE.setObjectName(u"graphicsView_E_hc_tabHE")
        self.graphicsView_E_hc_tabHE.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_53.addWidget(self.graphicsView_E_hc_tabHE, 0, 0, 1, 1)

        self.tabWidget_8.addTab(self.tab_27, "")
        self.tab_28 = QWidget()
        self.tab_28.setObjectName(u"tab_28")
        self.gridLayout_54 = QGridLayout(self.tab_28)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.graphicsView_E_Index_tabHE = QGraphicsView(self.tab_28)
        self.graphicsView_E_Index_tabHE.setObjectName(u"graphicsView_E_Index_tabHE")
        self.graphicsView_E_Index_tabHE.setCacheMode(QGraphicsView.CacheNone)

        self.gridLayout_54.addWidget(self.graphicsView_E_Index_tabHE, 0, 0, 1, 1)

        self.tabWidget_8.addTab(self.tab_28, "")

        self.gridLayout_47.addWidget(self.tabWidget_8, 0, 0, 1, 1)

        self.graphicsView_tab_TipAreaFunction_4.addTab(self.tab_24, "")

        self.gridLayout_48.addWidget(self.graphicsView_tab_TipAreaFunction_4, 5, 1, 1, 11)

        self.groupBox_20 = QGroupBox(self.tab_15)
        self.groupBox_20.setObjectName(u"groupBox_20")
        sizePolicy.setHeightForWidth(self.groupBox_20.sizePolicy().hasHeightForWidth())
        self.groupBox_20.setSizePolicy(sizePolicy)
        self.gridLayout_40 = QGridLayout(self.groupBox_20)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.spinBox_min_size_fluctuation_tabHE = QSpinBox(self.groupBox_20)
        self.spinBox_min_size_fluctuation_tabHE.setObjectName(u"spinBox_min_size_fluctuation_tabHE")
        sizePolicy.setHeightForWidth(self.spinBox_min_size_fluctuation_tabHE.sizePolicy().hasHeightForWidth())
        self.spinBox_min_size_fluctuation_tabHE.setSizePolicy(sizePolicy)
        self.spinBox_min_size_fluctuation_tabHE.setValue(1)

        self.gridLayout_40.addWidget(self.spinBox_min_size_fluctuation_tabHE, 1, 6, 1, 1)

        self.doubleSpinBox_zeroGradDelta_tabHE = QDoubleSpinBox(self.groupBox_20)
        self.doubleSpinBox_zeroGradDelta_tabHE.setObjectName(u"doubleSpinBox_zeroGradDelta_tabHE")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zeroGradDelta_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zeroGradDelta_tabHE.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zeroGradDelta_tabHE.setDecimals(4)
        self.doubleSpinBox_zeroGradDelta_tabHE.setValue(0.010000000000000)

        self.gridLayout_40.addWidget(self.doubleSpinBox_zeroGradDelta_tabHE, 1, 4, 1, 1)

        self.doubleSpinBox_Start_Pmax_tabHE = QDoubleSpinBox(self.groupBox_20)
        self.doubleSpinBox_Start_Pmax_tabHE.setObjectName(u"doubleSpinBox_Start_Pmax_tabHE")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_Start_Pmax_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Start_Pmax_tabHE.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Start_Pmax_tabHE.setValue(1.000000000000000)

        self.gridLayout_40.addWidget(self.doubleSpinBox_Start_Pmax_tabHE, 0, 4, 1, 1)

        self.label_49 = QLabel(self.groupBox_20)
        self.label_49.setObjectName(u"label_49")
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)

        self.gridLayout_40.addWidget(self.label_49, 1, 5, 1, 1)

        self.doubleSpinBox_End_Pmax_tabHE = QDoubleSpinBox(self.groupBox_20)
        self.doubleSpinBox_End_Pmax_tabHE.setObjectName(u"doubleSpinBox_End_Pmax_tabHE")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_End_Pmax_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_End_Pmax_tabHE.setSizePolicy(sizePolicy)
        self.doubleSpinBox_End_Pmax_tabHE.setValue(0.500000000000000)

        self.gridLayout_40.addWidget(self.doubleSpinBox_End_Pmax_tabHE, 0, 6, 1, 1)

        self.label_51 = QLabel(self.groupBox_20)
        self.label_51.setObjectName(u"label_51")
        sizePolicy.setHeightForWidth(self.label_51.sizePolicy().hasHeightForWidth())
        self.label_51.setSizePolicy(sizePolicy)

        self.gridLayout_40.addWidget(self.label_51, 0, 5, 1, 1)

        self.label_48 = QLabel(self.groupBox_20)
        self.label_48.setObjectName(u"label_48")
        sizePolicy.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy)

        self.gridLayout_40.addWidget(self.label_48, 0, 1, 1, 1)

        self.label_50 = QLabel(self.groupBox_20)
        self.label_50.setObjectName(u"label_50")
        sizePolicy.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy)

        self.gridLayout_40.addWidget(self.label_50, 1, 1, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_20, 3, 3, 1, 1)

        self.groupBox_18 = QGroupBox(self.tab_15)
        self.groupBox_18.setObjectName(u"groupBox_18")
        sizePolicy7.setHeightForWidth(self.groupBox_18.sizePolicy().hasHeightForWidth())
        self.groupBox_18.setSizePolicy(sizePolicy7)
        self.gridLayout_38 = QGridLayout(self.groupBox_18)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.label_65 = QLabel(self.groupBox_18)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_38.addWidget(self.label_65, 1, 0, 1, 1)

        self.lineEdit_MaterialName_tabHE = QLineEdit(self.groupBox_18)
        self.lineEdit_MaterialName_tabHE.setObjectName(u"lineEdit_MaterialName_tabHE")
        sizePolicy8.setHeightForWidth(self.lineEdit_MaterialName_tabHE.sizePolicy().hasHeightForWidth())
        self.lineEdit_MaterialName_tabHE.setSizePolicy(sizePolicy8)
        self.lineEdit_MaterialName_tabHE.setMinimumSize(QSize(300, 0))

        self.gridLayout_38.addWidget(self.lineEdit_MaterialName_tabHE, 0, 1, 1, 1)

        self.frame_6 = QFrame(self.groupBox_18)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_38.addWidget(self.frame_6, 0, 4, 1, 1)

        self.doubleSpinBox_Poisson_tabHE = QDoubleSpinBox(self.groupBox_18)
        self.doubleSpinBox_Poisson_tabHE.setObjectName(u"doubleSpinBox_Poisson_tabHE")
        sizePolicy8.setHeightForWidth(self.doubleSpinBox_Poisson_tabHE.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Poisson_tabHE.setSizePolicy(sizePolicy8)
        self.doubleSpinBox_Poisson_tabHE.setDecimals(3)
        self.doubleSpinBox_Poisson_tabHE.setValue(0.179000000000000)

        self.gridLayout_38.addWidget(self.doubleSpinBox_Poisson_tabHE, 0, 3, 1, 1)

        self.label_67 = QLabel(self.groupBox_18)
        self.label_67.setObjectName(u"label_67")
        sizePolicy3.setHeightForWidth(self.label_67.sizePolicy().hasHeightForWidth())
        self.label_67.setSizePolicy(sizePolicy3)

        self.gridLayout_38.addWidget(self.label_67, 0, 2, 1, 1)

        self.label_66 = QLabel(self.groupBox_18)
        self.label_66.setObjectName(u"label_66")
        sizePolicy3.setHeightForWidth(self.label_66.sizePolicy().hasHeightForWidth())
        self.label_66.setSizePolicy(sizePolicy3)

        self.gridLayout_38.addWidget(self.label_66, 0, 0, 1, 1)

        self.lineEdit_path_tabHE = QLineEdit(self.groupBox_18)
        self.lineEdit_path_tabHE.setObjectName(u"lineEdit_path_tabHE")
        sizePolicy17.setHeightForWidth(self.lineEdit_path_tabHE.sizePolicy().hasHeightForWidth())
        self.lineEdit_path_tabHE.setSizePolicy(sizePolicy17)

        self.gridLayout_38.addWidget(self.lineEdit_path_tabHE, 1, 1, 1, 4)


        self.gridLayout_48.addWidget(self.groupBox_18, 0, 0, 1, 12)

        self.groupBox_24 = QGroupBox(self.tab_15)
        self.groupBox_24.setObjectName(u"groupBox_24")
        sizePolicy3.setHeightForWidth(self.groupBox_24.sizePolicy().hasHeightForWidth())
        self.groupBox_24.setSizePolicy(sizePolicy3)
        self.groupBox_24.setMinimumSize(QSize(200, 0))
        self.gridLayout_49 = QGridLayout(self.groupBox_24)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.lineEdit_FrameCompliance_tabHE = QLineEdit(self.groupBox_24)
        self.lineEdit_FrameCompliance_tabHE.setObjectName(u"lineEdit_FrameCompliance_tabHE")
        self.lineEdit_FrameCompliance_tabHE.setReadOnly(True)

        self.gridLayout_49.addWidget(self.lineEdit_FrameCompliance_tabHE, 0, 0, 1, 1)

        self.Copy_FrameCompliance_tabHE = QPushButton(self.groupBox_24)
        self.Copy_FrameCompliance_tabHE.setObjectName(u"Copy_FrameCompliance_tabHE")

        self.gridLayout_49.addWidget(self.Copy_FrameCompliance_tabHE, 1, 0, 1, 1)


        self.gridLayout_48.addWidget(self.groupBox_24, 3, 0, 1, 1)

        self.tabWidget_5.addTab(self.tab_15, "")

        self.gridLayout_27.addWidget(self.tabWidget_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_13, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1220, 22))
        self.menuData = QMenu(self.menuBar)
        self.menuData.setObjectName(u"menuData")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuData.menuAction())
        self.menuData.addAction(self.actionnew)
        self.menuData.addAction(self.actionopen)
        self.menuData.addAction(self.actionSave)
        self.menuData.addAction(self.actionSaveAs)
        self.menuData.addAction(self.actionExport)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)
        self.graphicsView_tab_TipAreaFunction.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)
        self.graphicsView_tab_TipAreaFunction_2.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.graphicsView_tab_TipAreaFunction_5.setCurrentIndex(1)
        self.tabWidget_9.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(1)
        self.graphicsView_tab_TipAreaFunction_3.setCurrentIndex(1)
        self.tabWidget_6.setCurrentIndex(0)
        self.graphicsView_tab_TipAreaFunction_4.setCurrentIndex(2)
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.setCurrentIndex(0)
        self.tabWidget_7.setCurrentIndex(1)
        self.tabWidget_8.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionnew.setText(QCoreApplication.translate("MainWindow", u"New File...", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"Open File...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
#if QT_CONFIG(shortcut)
        self.actionExport.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"List of Tests :", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Find Surface", None))
        self.checkBox_UsingRate2findSurface_tabTAF.setText(QCoreApplication.translate("MainWindow", u"Using Critial (dP/dh)[mN/\u00b5m]", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Test Parameters", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"G200X", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.comboBox_method_tabCalibration.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Unloading", None))
        self.comboBox_method_tabCalibration.setItemText(1, QCoreApplication.translate("MainWindow", u"Multi Unloadings", None))
        self.comboBox_method_tabCalibration.setItemText(2, QCoreApplication.translate("MainWindow", u"CSM", None))

        self.OK_path_tabCalibration.setText(QCoreApplication.translate("MainWindow", u"Calcultate Frame Compliance and TAF", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Material (Target values)", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Material's Name:", None))
        self.lineEdit_MaterialName_tabTAF.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Young's Modulus[GPa]", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.lineEdit_path_tabCalibration.setText(QCoreApplication.translate("MainWindow", u"Examples\\Example1\\FusedSilica.xlsx", None))
        ___qtablewidgetitem = self.tableWidget_tabTAF.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Test Name", None));
        ___qtablewidgetitem1 = self.tableWidget_tabTAF.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Indentify?", None));
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Identify Loading-Holding-UnloadingStart-UnloadingEnd", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"End [100% of Pmax]", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Start [100% of Pmax]", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"min. Size of fluctuation", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Critial (dP/dt) [mN/s] ", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Data range to calculate Frame Compliance", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"min. Depth [\u00b5m]", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"min. Force [mN]", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Tip", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Number of Terms used for Tip Area Function", None))
        self.lineEdit_TipName_tabTAF.setText(QCoreApplication.translate("MainWindow", u"a Berkovich Tip", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Young's Modulus[GPa]", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"Tip's Name:", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio", None))
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTAF.setText(QCoreApplication.translate("MainWindow", u"show the Indentification of Loading-Holding-UnladingStart-UnladingEnd", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTAF.setText(QCoreApplication.translate("MainWindow", u"show find surface", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"inclusive of frame compliance", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"exclusive of frame compliance", None))
        self.graphicsView_tab_TipAreaFunction.setTabText(self.graphicsView_tab_TipAreaFunction.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Check unloading fitting", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Frame Stiffness [mN/\u00b5m]", None))
        self.lineEdit_FrameStiffness_Calibration.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Frame Compliance [\u00b5m/mN]", None))
        self.graphicsView_tab_TipAreaFunction.setTabText(self.graphicsView_tab_TipAreaFunction.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Frame Compliance", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Calibrated Tip Area Function", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/4</span>+</p></body></html>", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/2</span>+</p></body></html>", None))
        self.lineEdit_TAF1_tabTAF.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_TAF4_tabTAF.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span>+</p></body></html>", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Ac=", None))
        self.lineEdit_TAF5_tabTAF.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_TAF3_tabTAF.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">2</span>+</p></body></html>", None))
        self.lineEdit_TAF2_tabTAF.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/8</span></p></body></html>", None))
        self.graphicsView_tab_TipAreaFunction.setTabText(self.graphicsView_tab_TipAreaFunction.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tip Area Function", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calibration), QCoreApplication.translate("MainWindow", u"Tip Area Function", None))
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"show the Indentification of Loading-Holding-UnladingStart-UnladingEnd", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"show find surface", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"inclusive of frame compliance", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"exclusive of frame compliance", None))
        self.graphicsView_tab_TipAreaFunction_2.setTabText(self.graphicsView_tab_TipAreaFunction_2.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"Check unloading fitting", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Frame Compliance [\u00b5m/mN]", None))
        self.lineEdit_FrameStiffness_tabTipRadius_FrameStiffness.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Frame Stiffness [mN/\u00b5m]", None))
        self.graphicsView_tab_TipAreaFunction_2.setTabText(self.graphicsView_tab_TipAreaFunction_2.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Frame Compliance", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Identify Loading-Holding-UnloadingStart-UnloadingEnd", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"End [100% of Pmax]", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"min. Size of fluctuation", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Critial (dP/dt) [mN/s]", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Start [100% of Pmax]", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Test Parameters", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.comboBox_Equipment_tabTipRadius_FrameStiffness.setItemText(0, QCoreApplication.translate("MainWindow", u"G200X", None))

        self.comboBox_method_tabTipRadius_FrameStiffness.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Unloading", None))
        self.comboBox_method_tabTipRadius_FrameStiffness.setItemText(1, QCoreApplication.translate("MainWindow", u"Multi Unloadings", None))
        self.comboBox_method_tabTipRadius_FrameStiffness.setItemText(2, QCoreApplication.translate("MainWindow", u"CSM", None))

        ___qtablewidgetitem2 = self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Test Name", None));
        ___qtablewidgetitem3 = self.tableWidget_tabTipRadius_FrameStiffness.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Indentify?", None));
        self.pushButton_Calculate_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Calculate Frame Compliance", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"List of Tests :", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Data range to calculate Frame Compliance", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"min. Depth [\u00b5m]", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"min. Force [mN]", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Find Surface", None))
        self.checkBox_UsingRate2findSurface_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Using Critial (dP/dh)[mN/\u00b5m] ", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Path", None))
        self.lineEdit_path_tabTipRadius_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Examples\\Example2\\Tungsten_FrameStiffness.xlsx", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Calculate Frame Compliance", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Tested Material", None))
        self.label_73.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.label_75.setText(QCoreApplication.translate("MainWindow", u"Material's Name:", None))
        self.label_83.setText(QCoreApplication.translate("MainWindow", u"Young's Modulus [GPa]", None))
        self.label_74.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio", None))
        self.lineEdit_path_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"Examples\\Example2\\Tungsten_TipRadius.xlsx", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Find Surface", None))
        self.checkBox_UsingRate2findSurface_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"Using Critial (dP/dh) [mN/\u00b5m]", None))
        self.checkBox_iLHU_inclusive_frame_stiffness_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"show the Indentification of Loading-Holding-UnladingStart-UnladingEnd", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"show find surface", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_30), QCoreApplication.translate("MainWindow", u"inclusive of frame compliance", None))
        self.tabWidget_9.setTabText(self.tabWidget_9.indexOf(self.tab_31), QCoreApplication.translate("MainWindow", u"exclusive of frame compliance", None))
        self.graphicsView_tab_TipAreaFunction_5.setTabText(self.graphicsView_tab_TipAreaFunction_5.indexOf(self.tab_29), QCoreApplication.translate("MainWindow", u"Check load depth curve", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabTipRadius_2.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.graphicsView_tab_TipAreaFunction_5.setTabText(self.graphicsView_tab_TipAreaFunction_5.indexOf(self.tab_32), QCoreApplication.translate("MainWindow", u"Hertzian fitting", None))
        self.label_80.setText(QCoreApplication.translate("MainWindow", u"Tip Radius [\u00b5m]", None))
        self.label_84.setText(QCoreApplication.translate("MainWindow", u"+-", None))
        self.label_81.setText(QCoreApplication.translate("MainWindow", u"reduced Modulus Er [GPa]", None))
        self.graphicsView_tab_TipAreaFunction_5.setTabText(self.graphicsView_tab_TipAreaFunction_5.indexOf(self.tab_33), QCoreApplication.translate("MainWindow", u"Calculated Tip Radius", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Test Parameters", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.comboBox_Equipment_tabTipRadius.setItemText(0, QCoreApplication.translate("MainWindow", u"G200X", None))

        self.label_72.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.comboBox_method_tabTipRadius.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Unloading", None))
        self.comboBox_method_tabTipRadius.setItemText(1, QCoreApplication.translate("MainWindow", u"Multi Unloadings", None))
        self.comboBox_method_tabTipRadius.setItemText(2, QCoreApplication.translate("MainWindow", u"CSM", None))

        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Identify Loading-Holding-UnloadingStart-UnloadingEnd", None))
        self.label_76.setText(QCoreApplication.translate("MainWindow", u"End [100% of Pmax]", None))
        self.label_77.setText(QCoreApplication.translate("MainWindow", u"Start [100% of Pmax]", None))
        self.label_78.setText(QCoreApplication.translate("MainWindow", u"min. Size of fluctuation", None))
        self.label_79.setText(QCoreApplication.translate("MainWindow", u"Critial (dP/dt) [mN/s] ", None))
        self.label_82.setText(QCoreApplication.translate("MainWindow", u"List of Tests :", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Tip", None))
        self.lineEdit_TipName_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"a Berkovich Tip", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Young's Modulus [GPa]", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"Tip's Name:", None))
        self.pushButton_Calculate_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"Calculate Tip Radius", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Frame Compliance [\u00b5m/mN]", None))
        self.lineEdit_FrameCompliance_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.Copy_FrameCompliance_tabTipRadius.setText(QCoreApplication.translate("MainWindow", u"Copy the calculated value", None))
        ___qtablewidgetitem4 = self.tableWidget_tabTipRadius.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Test Name", None));
        ___qtablewidgetitem5 = self.tableWidget_tabTipRadius.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Indentify?", None));
        ___qtablewidgetitem6 = self.tableWidget_tabTipRadius.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Pop-in?", None));
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Calculate Tip Radius", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Tip Radius", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"Data range to calculate Frame Compliance", None))
        self.label_68.setText(QCoreApplication.translate("MainWindow", u"min. Depth [\u00b5m]", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"min. Force [mN]", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"List of Tests :", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Identify Loading-Holding-UnloadingStart-UnloadingEnd", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Start [100% of Pmax]", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"min. Size of fluctuation", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Critial (dP/dt) [mN/s]", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"End [100% of Pmax]", None))
        ___qtablewidgetitem7 = self.tableWidget_tabHE_FrameStiffness.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Test Name", None));
        ___qtablewidgetitem8 = self.tableWidget_tabHE_FrameStiffness.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Indentify?", None));
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Find Surface", None))
        self.checkBox_UsingRate2findSurface_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Using Critial (dP/dh)[mN/\u00b5m] ", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Test Parameters", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.comboBox_Equipment_tabHE_FrameStiffness.setItemText(0, QCoreApplication.translate("MainWindow", u"G200X", None))

        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.comboBox_method_tabHE_FrameStiffness.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Unloading", None))
        self.comboBox_method_tabHE_FrameStiffness.setItemText(1, QCoreApplication.translate("MainWindow", u"Multi Unloadings", None))
        self.comboBox_method_tabHE_FrameStiffness.setItemText(2, QCoreApplication.translate("MainWindow", u"CSM", None))

        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Path", None))
        self.lineEdit_path_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Examples\\Example1\\FusedSilica.xlsx", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"show the Indentification of Loading-Holding-UnladingStart-UnladingEnd", None))
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"show find surface", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_17), QCoreApplication.translate("MainWindow", u"inclusive of frame compliance", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_18), QCoreApplication.translate("MainWindow", u"exclusive of frame compliance", None))
        self.graphicsView_tab_TipAreaFunction_3.setTabText(self.graphicsView_tab_TipAreaFunction_3.indexOf(self.tab_16), QCoreApplication.translate("MainWindow", u"Check unloading fitting", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Frame Stiffness [mN/\u00b5m]", None))
        self.lineEdit_FrameStiffness_tabHE_FrameStiffness.setText("")
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Frame Compliance [\u00b5m/mN]", None))
        self.graphicsView_tab_TipAreaFunction_3.setTabText(self.graphicsView_tab_TipAreaFunction_3.indexOf(self.tab_19), QCoreApplication.translate("MainWindow", u"Frame Compliance", None))
        self.pushButton_Calculate_tabHE_FrameStiffness.setText(QCoreApplication.translate("MainWindow", u"Calculate Frame Compliance", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_14), QCoreApplication.translate("MainWindow", u"Calculate Frame Compliance", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Tip", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/8</span></p></body></html>", None))
        self.lineEdit_TAF4_tabHE.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_TAF3_tabHE.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Ac=", None))
        self.lineEdit_TAF1_tabHE.setText(QCoreApplication.translate("MainWindow", u"24.5", None))
        self.lineEdit_TAF2_tabHE.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">2</span>+</p></body></html>", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span>+</p></body></html>", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/2</span>+</p></body></html>", None))
        self.lineEdit_TAF5_tabHE.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>h<span style=\" vertical-align:sub;\">c</span><span style=\" vertical-align:super;\">1/4</span>+</p></body></html>", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Calibrated TAF:", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Tip Name:", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio:", None))
        self.Copy_TAF_tabHE.setText(QCoreApplication.translate("MainWindow", u"Copy from\n"
"\"Tip Area Function\"", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Young's Modulus [GPa]:", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Find Surface", None))
        self.checkBox_UsingRate2findSurface_tabHE.setText(QCoreApplication.translate("MainWindow", u"Using Critial (dP/dh)[mN/\u00b5m]", None))
        self.Calculate_tabHE.setText(QCoreApplication.translate("MainWindow", u"Calculate Hardness and Modulus", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Test Parameters", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.comboBox_Equipment_tabHE.setItemText(0, QCoreApplication.translate("MainWindow", u"G200X", None))

        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.comboBox_method_tabHE.setItemText(0, QCoreApplication.translate("MainWindow", u"Single Unloading", None))
        self.comboBox_method_tabHE.setItemText(1, QCoreApplication.translate("MainWindow", u"Multi Unloadings", None))
        self.comboBox_method_tabHE.setItemText(2, QCoreApplication.translate("MainWindow", u"CSM", None))

        ___qtablewidgetitem9 = self.tableWidget_tabHE.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Test Name", None));
        ___qtablewidgetitem10 = self.tableWidget_tabHE.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Indentify?", None));
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"List of Tests :", None))
        self.pushButton_plot_chosen_test_tab_inclusive_frame_stiffness_tabHE.setText(QCoreApplication.translate("MainWindow", u"Plot the selected Test (by clicking on the test in the \"List of Tests\")", None))
        self.checkBox_iLHU_inclusive_frame_stiffness_tabHE.setText(QCoreApplication.translate("MainWindow", u"show the Indentification of Loading-Holding-UnladingStart-UnladingEnd", None))
        self.checkBox_showFindSurface_tab_inclusive_frame_stiffness_tabHE.setText(QCoreApplication.translate("MainWindow", u"show find surface", None))
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.setTabText(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.indexOf(self.tab_21), QCoreApplication.translate("MainWindow", u"inclusive of frame stiffness", None))
        self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.setTabText(self.graphicsView_load_depth_tab_exclusive_frame_stiffness_tabHE.indexOf(self.tab_22), QCoreApplication.translate("MainWindow", u"exclusive of frame stiffness", None))
        self.graphicsView_tab_TipAreaFunction_4.setTabText(self.graphicsView_tab_TipAreaFunction_4.indexOf(self.tab_20), QCoreApplication.translate("MainWindow", u"Check unloading fitting", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_25), QCoreApplication.translate("MainWindow", u"Hardness-contact depth", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_26), QCoreApplication.translate("MainWindow", u"Hardness-Indents' number", None))
        self.graphicsView_tab_TipAreaFunction_4.setTabText(self.graphicsView_tab_TipAreaFunction_4.indexOf(self.tab_23), QCoreApplication.translate("MainWindow", u"Hardness", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_27), QCoreApplication.translate("MainWindow", u"Young's Modulus-contact depth", None))
        self.tabWidget_8.setTabText(self.tabWidget_8.indexOf(self.tab_28), QCoreApplication.translate("MainWindow", u"Young's Modulus-Indents' number", None))
        self.graphicsView_tab_TipAreaFunction_4.setTabText(self.graphicsView_tab_TipAreaFunction_4.indexOf(self.tab_24), QCoreApplication.translate("MainWindow", u"Young's Modulus", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Identify Loading-Holding-UnloadingStart-UnloadingEnd", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"min. Size of fluctuation", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"End [100% of Pmax]", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Start [100% of Pmax]", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Critial (dP/dt) [mN/s]", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Tested Material", None))
        self.label_65.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Poisson's ratio", None))
        self.label_66.setText(QCoreApplication.translate("MainWindow", u"Material's Name:", None))
        self.lineEdit_path_tabHE.setText(QCoreApplication.translate("MainWindow", u"Examples\\Example1\\FusedSilica.xlsx", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Frame Compliance [\u00b5m/mN]", None))
        self.lineEdit_FrameCompliance_tabHE.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.Copy_FrameCompliance_tabHE.setText(QCoreApplication.translate("MainWindow", u"Copy the calculated value", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_15), QCoreApplication.translate("MainWindow", u"Calculate Hardness and Modulus", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_13), QCoreApplication.translate("MainWindow", u"Hardness and Young's Modulus", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

