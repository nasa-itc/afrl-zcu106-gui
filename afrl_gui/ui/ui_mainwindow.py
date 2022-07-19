# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTabWidget, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 508)
        self.action_file_new_qemu_instance = QAction(MainWindow)
        self.action_file_new_qemu_instance.setObjectName(u"action_file_new_qemu_instance")
        self.action_help_about = QAction(MainWindow)
        self.action_help_about.setObjectName(u"action_help_about")
        self.action_file_exit = QAction(MainWindow)
        self.action_file_exit.setObjectName(u"action_file_exit")
        self.actionModify_Image_Contents = QAction(MainWindow)
        self.actionModify_Image_Contents.setObjectName(u"actionModify_Image_Contents")
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.ghLogoLabel = QLabel(self.widget)
        self.ghLogoLabel.setObjectName(u"ghLogoLabel")
        self.ghLogoLabel.setGeometry(QRect(560, 350, 100, 100))
        self.jstarLogoLabel = QLabel(self.widget)
        self.jstarLogoLabel.setObjectName(u"jstarLogoLabel")
        self.jstarLogoLabel.setGeometry(QRect(690, 340, 220, 100))
        self.terminalTabWidget = QTabWidget(self.widget)
        self.terminalTabWidget.setObjectName(u"terminalTabWidget")
        self.terminalTabWidget.setGeometry(QRect(20, 10, 531, 441))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.terminalTabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.terminalTabWidget.addTab(self.tab_2, "")
        self.qemuInstanceTable = QTableView(self.widget)
        self.qemuInstanceTable.setObjectName(u"qemuInstanceTable")
        self.qemuInstanceTable.setGeometry(QRect(560, 10, 581, 291))
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 22))
        self.menuAFRL_RWWN_QEMU_Launcher = QMenu(self.menubar)
        self.menuAFRL_RWWN_QEMU_Launcher.setObjectName(u"menuAFRL_RWWN_QEMU_Launcher")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAFRL_RWWN_QEMU_Launcher.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuAFRL_RWWN_QEMU_Launcher.addAction(self.action_file_new_qemu_instance)
        self.menuAFRL_RWWN_QEMU_Launcher.addSeparator()
        self.menuAFRL_RWWN_QEMU_Launcher.addAction(self.actionModify_Image_Contents)
        self.menuAFRL_RWWN_QEMU_Launcher.addAction(self.action_file_exit)
        self.menuHelp.addAction(self.action_help_about)

        self.retranslateUi(MainWindow)

        self.terminalTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_file_new_qemu_instance.setText(QCoreApplication.translate("MainWindow", u"New QEMU Instance", None))
        self.action_help_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_file_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionModify_Image_Contents.setText(QCoreApplication.translate("MainWindow", u"Modify Image Contents", None))
#if QT_CONFIG(tooltip)
        self.actionModify_Image_Contents.setToolTip(QCoreApplication.translate("MainWindow", u"Opens GUI to copy items into guest image", None))
#endif // QT_CONFIG(tooltip)
        self.ghLogoLabel.setText("")
        self.jstarLogoLabel.setText("")
        self.terminalTabWidget.setTabText(self.terminalTabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.terminalTabWidget.setTabText(self.terminalTabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menuAFRL_RWWN_QEMU_Launcher.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

