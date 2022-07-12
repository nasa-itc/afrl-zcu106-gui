# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# 
# This software is provided "as is" without any warranty of any kind, either expressed, implied, or statutory, including, but not
# limited to, any warranty that the software will conform to specifications, any implied warranties of merchantability, fitness
# for a particular purpose, and freedom from infringement, and any warranty that the documentation will conform to the program, or
# any warranty that the software will be error free.
# 
# In no event shall NASA be liable for any damages, including, but not limited to direct, indirect, special or consequential damages,
# arising out of, resulting from, or in any way connected with the software or its documentation, whether or not based upon warranty,
# contract, tort or otherwise, and whether or not loss was sustained from, or arose out of the results of, or use of, the software,
# documentation or services provided hereunder.
# 
# ITC Team
# NASA IV&V
# ivv-itc@lists.nasa.gov

import time
import datetime
import os.path

from PySide6.QtWidgets import QMainWindow, QLabel, QMessageBox, \
    QGraphicsView, QGraphicsScene, QWidget, QDockWidget, QTableView
from PySide6.QtGui import QGuiApplication, QIcon, QPixmap, QRegularExpressionValidator, \
    QIntValidator, QAction
from PySide6.QtCore import Signal, Qt, Slot, QRect

from afrl_gui import __version__
from afrl_gui.common import RESOURCE_ROOT, MAXIMUM_QEMU_INSTANCES
from afrl_gui.ui.ui_mainwindow import Ui_MainWindow
from afrl_gui.qemulaunchwizard import QemuLaunchWizard
from afrl_gui.qemuinstance import qemuInstance
from afrl_gui.terminalwidget import terminalWidget
from afrl_gui.qemutableviewmodel import qemuTableViewModel
from afrl_gui.devicelistviewmodel import deviceListViewModel

class MainWindow(QMainWindow):

    kill_thread = Signal()

    def __init__(self, app):
        self.app = app
        self.paused = False
        super().__init__()
        self.tableModel = qemuTableViewModel()
        self.deviceListModel = deviceListViewModel();
        self.window = []
        self.default_theme = QGuiApplication.palette()
        self.qemuList = []
        self.init_ui()

    def init_ui(self):
        """init ui"""
        # load ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AFRL-RWWN QEMU MANAGER")

        # Update logos
        logo = QPixmap(os.path.join(RESOURCE_ROOT, "golden-horde_seal-300x300.png"))
        logo = logo.scaled(100, 100, Qt.KeepAspectRatio)
        self.ui.ghLogoLabel.setPixmap(logo)

        logo = QPixmap(os.path.join(RESOURCE_ROOT, "jstar_logo_final.jpg"))
        logo = logo.scaled(200, 100, Qt.KeepAspectRatio)       # menus
        self.ui.jstarLogoLabel.setPixmap(logo)

        # Setup Menu Actions
        self.ui.action_file_new_qemu_instance.triggered.connect(self.show_launch_wizard)
        self.ui.action_file_exit.triggered.connect(self.close)
        self.ui.action_help_about.triggered.connect(self.show_about_splash)

        # Initialize QEMU Instance Table
        self.init_table()

        # Load xterm terminal into the terminal widget
        self.ui.terminalTabWidget.clear()  # clear the default tabs
        self.init_terminalView(0, "QEMU 1")
        self.init_terminalView(1, "QEMU 2")

    def init_table(self):
        """initializes table headers"""
        headerData = self.tableModel.headerData(0, Qt.Horizontal)
        for row in range(0, MAXIMUM_QEMU_INSTANCES):
            qemuNode = qemuInstance()
            self.tableModel.insertQemuInstance(qemuNode)
        print(f"header data: {headerData}")
        self.ui.qemuInstanceTable.setModel(self.tableModel)
        self.ui.qemuInstanceTable.setColumnWidth(0, 186)
        self.ui.qemuInstanceTable.setColumnWidth(1, 186)
        self.ui.qemuInstanceTable.setColumnWidth(2, 130)
        self.ui.qemuInstanceTable.setColumnWidth(3, 30)

    def init_terminalView(self, tabIndex, tabName):
        """initializes tab view with terminal windows for QEMU instances"""
        term = terminalWidget(self)
        tabSize = self.ui.terminalTabWidget.size()
        self.ui.terminalTabWidget.insertTab(tabIndex, term, tabName)
        self.ui.terminalTabWidget.tabCloseRequested.connect(
            term.termProcess.terminate)
        term.resize(tabSize)
        pid = term.startXterm()
        print(
            "Tab Size: " + str(tabSize)
            + "    TerminalSize: " + str(term.size())
            )
        return pid

    def show_launch_wizard(self):
        """start qemu instance launch wizard in dock"""
        if self.tableModel.validDataCount() < MAXIMUM_QEMU_INSTANCES:
            dock = QDockWidget(self)
            dock.setFloating(True)
            launchWiz = QemuLaunchWizard(dock)
            dock.setWidget(launchWiz)
            self.addDockWidget(Qt.LeftDockWidgetArea, dock)
            launchWiz.newQemuSignal.connect(self.tableModel.insertQemuInstance)
            launchWiz.newDeviceSignal.connect(self.deviceListModel.insertDevice)
            launchWiz.ui.deviceListView.setModel(self.deviceListModel)
        else:
            print("Error: All QEMU Instances Used")
            errBox = QMessageBox(self)
            errBox.setWindowTitle("QEMU Launch Error")
            errBox.setIcon(QMessageBox.Icon.Critical)
            errBox.setText("All QEMU Instances Utilized")
            errBox.exec_()

    def show_about_splash(self):
        """about menu handler"""
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("AFRL-RWWN QEMU MANAGER")
        about_dialog.setIconPixmap(QPixmap(
            os.path.join(RESOURCE_ROOT, 'nasa.png')))
        about_dialog.setTextFormat(Qt.RichText)
        about_dialog.setText(
            "<b>AFRL-RWWN QEMU MANAGER</b><br>"
            "Version: <em>" + __version__ + "</em><br><br>"
            "Copyright (C) 2022 National Aeronautics and Space Administration."
            "All Foreign Rights are Reserved to the U.S. Government."
            )
        about_dialog.exec_()
