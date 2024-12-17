# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homeworklNWtrR.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QTableView, QWidget)

class Ui_HMWindow(object):
    def setupUi(self, HMWindow):
        if not HMWindow.objectName():
            HMWindow.setObjectName(u"HMWindow")
        HMWindow.resize(1074, 714)
        HMWindow.setMinimumSize(QSize(1074, 714))
        HMWindow.setMaximumSize(QSize(1074, 714))
        HMWindow.setStyleSheet(u"background-color: #030303;")
        self.centralwidget = QWidget(HMWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 570, 1081, 151))
        self.frame.setStyleSheet(u"background-color: #0a0a0a;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.infoButton = QPushButton(self.frame)
        self.infoButton.setObjectName(u"infoButton")
        self.infoButton.setGeometry(QRect(190, 20, 101, 91))
        self.infoButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"	margin-top: 0;\n"
"}\n"
"QPushButton:hover{\n"
"	margin-top: 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.aiButton = QPushButton(self.frame)
        self.aiButton.setObjectName(u"aiButton")
        self.aiButton.setGeometry(QRect(390, 20, 101, 91))
        self.aiButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"	margin-top: 0;\n"
"}\n"
"QPushButton:hover{\n"
"	margin-top: 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.memoButton = QPushButton(self.frame)
        self.memoButton.setObjectName(u"memoButton")
        self.memoButton.setGeometry(QRect(590, 20, 101, 91))
        self.memoButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"	margin-top: 0;\n"
"}\n"
"QPushButton:hover{\n"
"	margin-top: 5px;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(790, 10, 101, 81))
        self.pushButton_4.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"	margin-top: 0;\n"
"}\n"
"QPushButton:hover{\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(210, -10, 661, 61))
        self.frame_2.setStyleSheet(u"background-color: #0a0a0a;\n"
"border:50px;\n"
"border-radius:10px;")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 20, 651, 31))
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(140, 80, 801, 461))
        self.frame_3.setStyleSheet(u"background-color: #0a0a0a;\n"
"border:50px;\n"
"border-radius:10px;")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.tableView = QTableView(self.frame_3)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 20, 781, 381))
        self.tableView.setMinimumSize(QSize(781, 381))
        self.tableView.setMaximumSize(QSize(781, 381))
        self.updateButton = QPushButton(self.frame_3)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(250, 410, 291, 41))
        self.updateButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #9785ff;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(280, 140, 241, 22))
        self.lineEdit.setStyleSheet(u"background-color: 0a0f0a")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 115, 231, 21))
        self.saveButton = QPushButton(self.frame_3)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(260, 260, 291, 41))
        self.saveButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #9785ff;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.tokenButton = QPushButton(self.frame_3)
        self.tokenButton.setObjectName(u"tokenButton")
        self.tokenButton.setGeometry(QRect(360, 166, 161, 20))
        self.tokenButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #9785ff;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.nextweekButton = QPushButton(self.frame_3)
        self.nextweekButton.setObjectName(u"nextweekButton")
        self.nextweekButton.setGeometry(QRect(560, 410, 211, 41))
        self.nextweekButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #9785ff;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.lastweekButton = QPushButton(self.frame_3)
        self.lastweekButton.setObjectName(u"lastweekButton")
        self.lastweekButton.setGeometry(QRect(20, 410, 211, 41))
        self.lastweekButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #9785ff;\n"
"}\n"
"QPushButton:pressed{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background-color: #5c66b1;\n"
"	font: 700 12pt \"Arial\";\n"
"}")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 50, 781, 31))
        HMWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HMWindow)

        QMetaObject.connectSlotsByName(HMWindow)
    # setupUi

    def retranslateUi(self, HMWindow):
        HMWindow.setWindowTitle(QCoreApplication.translate("HMWindow", u"SHelper", None))
        self.infoButton.setText(QCoreApplication.translate("HMWindow", u"\u0418\u043d\u0444\u043e", None))
        self.aiButton.setText(QCoreApplication.translate("HMWindow", u"\u0427\u0430\u0442 AI", None))
        self.memoButton.setText(QCoreApplication.translate("HMWindow", u"\u041f\u0430\u043c\u044f\u0442\u043a\u0438", None))
        self.pushButton_4.setText(QCoreApplication.translate("HMWindow", u"\u0414\u043e\u043c\u0430\u0448\u043d\u0435\u0435\n"
"\u0417\u0430\u0434\u0430\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("HMWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">\u0414\u041e\u041c\u0410\u0428\u041d\u0415\u0415 \u0417\u0410\u0414\u0410\u041d\u0418\u042f</span></p></body></html>", None))
        self.updateButton.setText(QCoreApplication.translate("HMWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("HMWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043b\u044e\u0447-\u0442\u043e\u043a\u0435\u043d", None))
        self.saveButton.setText(QCoreApplication.translate("HMWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.tokenButton.setText(QCoreApplication.translate("HMWindow", u"\u0423\u0437\u043d\u0430\u0442\u044c \u043a\u043b\u044e\u0447-\u0442\u043e\u043a\u0435\u043d", None))
        self.nextweekButton.setText(QCoreApplication.translate("HMWindow", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u043d\u0435\u0434\u0435\u043b\u044f", None))
        self.lastweekButton.setText(QCoreApplication.translate("HMWindow", u"\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0430\u044f \u043d\u0435\u0434\u0435\u043b\u044f", None))
        self.label_3.setText(QCoreApplication.translate("HMWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">c {date} \u043f\u043e {date2}</span></p></body></html>", None))
    # retranslateUi

