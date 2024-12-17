# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infoQUTiWy.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_InfoWindow(object):
    def setupUi(self, InfoWindow):
        if not InfoWindow.objectName():
            InfoWindow.setObjectName(u"InfoWindow")
        InfoWindow.resize(1074, 714)
        InfoWindow.setMinimumSize(QSize(1074, 714))
        InfoWindow.setMaximumSize(QSize(1074, 714))
        InfoWindow.setStyleSheet(u"background-color: #030303;")
        self.centralwidget = QWidget(InfoWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 570, 1081, 151))
        self.frame.setStyleSheet(u"background-color: #0a0a0a;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.infoButton = QPushButton(self.frame)
        self.infoButton.setObjectName(u"infoButton")
        self.infoButton.setGeometry(QRect(190, 10, 101, 81))
        self.infoButton.setStyleSheet(u"QPushButton{\n"
"	border:3px;\n"
"	border-radius:10px;\n"
"	background: #8593fe;\n"
"	font: 700 12pt \"Arial\";\n"
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
        self.homeworkButton = QPushButton(self.frame)
        self.homeworkButton.setObjectName(u"homeworkButton")
        self.homeworkButton.setGeometry(QRect(790, 20, 101, 91))
        self.homeworkButton.setStyleSheet(u"QPushButton{\n"
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
        self.frame_3.setGeometry(QRect(180, 80, 721, 461))
        self.frame_3.setStyleSheet(u"background-color: #0a0a0a;\n"
"border:50px;\n"
"border-radius:10px;")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 30, 691, 201))
        InfoWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(InfoWindow)

        QMetaObject.connectSlotsByName(InfoWindow)
    # setupUi

    def retranslateUi(self, InfoWindow):
        InfoWindow.setWindowTitle(QCoreApplication.translate("InfoWindow", u"SHelper", None))
        self.infoButton.setText(QCoreApplication.translate("InfoWindow", u"\u0418\u043d\u0444\u043e", None))
        self.aiButton.setText(QCoreApplication.translate("InfoWindow", u"\u0427\u0430\u0442 AI", None))
        self.memoButton.setText(QCoreApplication.translate("InfoWindow", u"\u041f\u0430\u043c\u044f\u0442\u043a\u0438", None))
        self.homeworkButton.setText(QCoreApplication.translate("InfoWindow", u"\u0414\u043e\u043c\u0430\u0448\u043d\u0435\u0435\n"
"\u0417\u0430\u0434\u0430\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("InfoWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">\u0413\u041b\u0410\u0412\u041d\u041e\u0415 \u041c\u0415\u041d\u042e</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("InfoWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">\u041f\u0440\u0438\u0432\u0435\u0442\u0441\u0442\u0432\u0443\u044e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c!<br/><br/>\u0410\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043f\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0443:<br/>https://github.com/Anarchowitz/SHelper<br/></span><span style=\" font-size:11pt;\">\u0410\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f: {version}</span></p></body></html>", None))
    # retranslateUi

