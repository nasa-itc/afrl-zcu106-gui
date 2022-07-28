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
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QHeaderView,
    QPushButton, QSizePolicy, QTreeView, QWidget)

class Ui_DiskImageWidget(object):
    def setupUi(self, DiskImageWidget):
        if not DiskImageWidget.objectName():
            DiskImageWidget.setObjectName(u"DiskImageWidget")
        DiskImageWidget.resize(1203, 574)
        DiskImageWidget.setFloating(True)
        DiskImageWidget.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.hostTreeView = QTreeView(self.dockWidgetContents)
        self.hostTreeView.setObjectName(u"hostTreeView")
        self.hostTreeView.setGeometry(QRect(10, 50, 500, 500))
        self.guestTreeView = QTreeView(self.dockWidgetContents)
        self.guestTreeView.setObjectName(u"guestTreeView")
        self.guestTreeView.setGeometry(QRect(690, 50, 500, 500))
        self.toHostPushButton = QPushButton(self.dockWidgetContents)
        self.toHostPushButton.setObjectName(u"toHostPushButton")
        self.toHostPushButton.setGeometry(QRect(520, 260, 151, 41))
        self.toGuestPushButton = QPushButton(self.dockWidgetContents)
        self.toGuestPushButton.setObjectName(u"toGuestPushButton")
        self.toGuestPushButton.setGeometry(QRect(520, 210, 151, 41))
        self.hostComboBox = QComboBox(self.dockWidgetContents)
        self.hostComboBox.setObjectName(u"hostComboBox")
        self.hostComboBox.setGeometry(QRect(10, 10, 500, 31))
        self.guestComboBox = QComboBox(self.dockWidgetContents)
        self.guestComboBox.setObjectName(u"guestComboBox")
        self.guestComboBox.setGeometry(QRect(690, 10, 500, 31))
        DiskImageWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DiskImageWidget)

        QMetaObject.connectSlotsByName(DiskImageWidget)
    # setupUi

    def retranslateUi(self, DiskImageWidget):
        DiskImageWidget.setWindowTitle(QCoreApplication.translate("DiskImageWidget", u"Modify Guest Image", None))
        self.toHostPushButton.setText("")
        self.toGuestPushButton.setText("")
    # retranslateUi

