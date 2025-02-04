# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chataikfmFyC.ui'
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
    QPushButton, QSizePolicy, QTextBrowser, QTextEdit,
    QWidget)
import shelper_rc

class Ui_AiWindow(object):
    def setupUi(self, AiWindow):
        if not AiWindow.objectName():
            AiWindow.setObjectName(u"AiWindow")
        AiWindow.resize(1074, 714)
        AiWindow.setMinimumSize(QSize(1074, 714))
        AiWindow.setMaximumSize(QSize(1074, 714))
        icon = QIcon()
        icon.addFile(u":/icons/C:/Users/user/Downloads/\u0432\u0430\u0440\u0438\u0430\u043d\u0442\u0438\u043a\u043e\u043d\u043a\u04381-_1_.ico", QSize(), QIcon.Normal, QIcon.Off)
        AiWindow.setWindowIcon(icon)
        AiWindow.setStyleSheet(u"background-color: #030303;")
        self.centralwidget = QWidget(AiWindow)
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
        self.aiButton.setGeometry(QRect(390, 10, 101, 81))
        self.aiButton.setStyleSheet(u"QPushButton{\n"
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
        self.frame_3.setGeometry(QRect(160, 80, 751, 481))
        self.frame_3.setStyleSheet(u"background-color: #0a0a0a;\n"
"border:50px;\n"
"border-radius:10px;")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.textEdit = QTextEdit(self.frame_3)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(40, 440, 531, 31))
        self.textEdit.setStyleSheet(u"background-color: #1a1a1a;\n"
"border:50px;\n"
"border-radius:10px;")
        self.sendButton = QPushButton(self.frame_3)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setGeometry(QRect(580, 440, 141, 31))
        self.sendButton.setStyleSheet(u"QPushButton{\n"
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
        self.sendButton.setAutoExclusive(False)
        self.textBrowser = QTextBrowser(self.frame_3)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 731, 421))
        AiWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AiWindow)

        QMetaObject.connectSlotsByName(AiWindow)
    # setupUi

    def retranslateUi(self, AiWindow):
        AiWindow.setWindowTitle(QCoreApplication.translate("AiWindow", u"SHelper", None))
        self.infoButton.setText(QCoreApplication.translate("AiWindow", u"\u0418\u043d\u0444\u043e", None))
        self.aiButton.setText(QCoreApplication.translate("AiWindow", u"\u041f\u043e\u043c\u043e\u0449\u043d\u0438\u043a", None))
        self.memoButton.setText(QCoreApplication.translate("AiWindow", u"\u041f\u0430\u043c\u044f\u0442\u043a\u0438", None))
        self.homeworkButton.setText(QCoreApplication.translate("AiWindow", u"\u0414\u043e\u043c\u0430\u0448\u043d\u0435\u0435\n"
"\u0417\u0430\u0434\u0430\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("AiWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">\u0427\u0410\u0422 \u0421 \u0423\u041c\u041d\u042b\u041c \u0414\u0420\u0423\u0413\u041e\u041c</span></p></body></html>", None))
        self.sendButton.setText(QCoreApplication.translate("AiWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

