# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diskimagewidget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QPushButton, QSizePolicy, QTreeView, QWidget)

class Ui_DiskImageWidget(object):
    def setupUi(self, DiskImageWidget):
        if not DiskImageWidget.objectName():
            DiskImageWidget.setObjectName(u"DiskImageWidget")
        DiskImageWidget.resize(1221, 608)
        self.toHostPushButton = QPushButton(DiskImageWidget)
        self.toHostPushButton.setObjectName(u"toHostPushButton")
        self.toHostPushButton.setGeometry(QRect(540, 330, 141, 41))
        self.toGuestPushButton = QPushButton(DiskImageWidget)
        self.toGuestPushButton.setObjectName(u"toGuestPushButton")
        self.toGuestPushButton.setGeometry(QRect(540, 280, 141, 41))
        self.frame = QFrame(DiskImageWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 40, 521, 561))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.hostTreeView = QTreeView(self.frame)
        self.hostTreeView.setObjectName(u"hostTreeView")
        self.hostTreeView.setGeometry(QRect(10, 50, 500, 500))
        self.hostComboBox = QComboBox(self.frame)
        self.hostComboBox.setObjectName(u"hostComboBox")
        self.hostComboBox.setGeometry(QRect(10, 10, 500, 31))
        self.frame_2 = QFrame(DiskImageWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(690, 40, 521, 561))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.guestTreeView = QTreeView(self.frame_2)
        self.guestTreeView.setObjectName(u"guestTreeView")
        self.guestTreeView.setGeometry(QRect(10, 50, 500, 500))
        self.guestComboBox = QComboBox(self.frame_2)
        self.guestComboBox.setObjectName(u"guestComboBox")
        self.guestComboBox.setGeometry(QRect(10, 10, 500, 31))
        self.detailsPushButton = QPushButton(DiskImageWidget)
        self.detailsPushButton.setObjectName(u"detailsPushButton")
        self.detailsPushButton.setGeometry(QRect(540, 400, 141, 41))
        self.frame_2.raise_()
        self.frame.raise_()
        self.toHostPushButton.raise_()
        self.toGuestPushButton.raise_()
        self.detailsPushButton.raise_()

        self.retranslateUi(DiskImageWidget)

        QMetaObject.connectSlotsByName(DiskImageWidget)
    # setupUi

    def retranslateUi(self, DiskImageWidget):
        DiskImageWidget.setWindowTitle(QCoreApplication.translate("DiskImageWidget", u"Modify Guest Image", None))
        self.toHostPushButton.setText("")
        self.toGuestPushButton.setText("")
        self.detailsPushButton.setText(QCoreApplication.translate("DiskImageWidget", u"Show Details", None))
    # retranslateUi

