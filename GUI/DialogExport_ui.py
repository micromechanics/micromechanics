# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogExport.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_DialogExport(object):
    def setupUi(self, DialogExport):
        if not DialogExport.objectName():
            DialogExport.setObjectName(u"DialogExport")
        DialogExport.resize(535, 142)
        self.gridLayout = QGridLayout(DialogExport)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_Format = QComboBox(DialogExport)
        self.comboBox_Format.addItem("")
        self.comboBox_Format.setObjectName(u"comboBox_Format")

        self.gridLayout.addWidget(self.comboBox_Format, 4, 2, 1, 1)

        self.lineEdit_ExportPath = QLineEdit(DialogExport)
        self.lineEdit_ExportPath.setObjectName(u"lineEdit_ExportPath")

        self.gridLayout.addWidget(self.lineEdit_ExportPath, 2, 2, 1, 1)

        self.label = QLabel(DialogExport)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_2 = QLabel(DialogExport)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.comboBox_Tab = QComboBox(DialogExport)
        self.comboBox_Tab.addItem("")
        self.comboBox_Tab.addItem("")
        self.comboBox_Tab.setObjectName(u"comboBox_Tab")

        self.gridLayout.addWidget(self.comboBox_Tab, 3, 2, 1, 1)

        self.pushButton_selectPath = QPushButton(DialogExport)
        self.pushButton_selectPath.setObjectName(u"pushButton_selectPath")

        self.gridLayout.addWidget(self.pushButton_selectPath, 2, 3, 1, 1)

        self.label_3 = QLabel(DialogExport)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.frame = QFrame(DialogExport)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 6, 0, 1, 4)

        self.pushButton_OK = QPushButton(DialogExport)
        self.pushButton_OK.setObjectName(u"pushButton_OK")
        self.pushButton_OK.setEnabled(True)

        self.gridLayout.addWidget(self.pushButton_OK, 5, 2, 1, 1)


        self.retranslateUi(DialogExport)

        QMetaObject.connectSlotsByName(DialogExport)
    # setupUi

    def retranslateUi(self, DialogExport):
        DialogExport.setWindowTitle(QCoreApplication.translate("DialogExport", u"Export ", None))
        self.comboBox_Format.setItemText(0, QCoreApplication.translate("DialogExport", u"Each Test in on sheet", None))

        self.label.setText(QCoreApplication.translate("DialogExport", u"Path", None))
        self.label_2.setText(QCoreApplication.translate("DialogExport", u"Tab", None))
        self.comboBox_Tab.setItemText(0, QCoreApplication.translate("DialogExport", u"Hardness and Young's Modulus", None))
        self.comboBox_Tab.setItemText(1, QCoreApplication.translate("DialogExport", u"Pop-in ", None))

        self.pushButton_selectPath.setText(QCoreApplication.translate("DialogExport", u"select", None))
        self.label_3.setText(QCoreApplication.translate("DialogExport", u"Format", None))
        self.pushButton_OK.setText(QCoreApplication.translate("DialogExport", u"Export", None))
    # retranslateUi

