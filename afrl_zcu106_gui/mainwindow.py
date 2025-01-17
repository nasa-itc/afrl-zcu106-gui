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
import docker
import os.path

from PyQt5.QtWidgets import QAction, QMainWindow, QLabel, QMessageBox, \
    QInputDialog, QGraphicsView, QGraphicsScene, QWidget, QDockWidget, QTableView, QScrollArea
from PyQt5.QtGui import QGuiApplication, QIcon, QPixmap, QRegularExpressionValidator, \
    QIntValidator, QPalette
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QRect

from afrl_zcu106_gui import __version__
from afrl_zcu106_gui.common import RESOURCE_ROOT, MAXIMUM_QEMU_INSTANCES, DOCKER_ROOT, DOCKER_TIMEOUT
from afrl_zcu106_gui.ui.ui_mainwindow import Ui_MainWindow
from afrl_zcu106_gui.qemulaunchwizard import QemuLaunchWizard
from afrl_zcu106_gui.qemuinstance import qemuInstance
from afrl_zcu106_gui.terminalwidget import terminalWidget
from afrl_zcu106_gui.qemutableviewmodel import qemuTableViewModel
from afrl_zcu106_gui.devicelistviewmodel import deviceListViewModel
from afrl_zcu106_gui.diskimagewidget import diskImageWidget
from afrl_zcu106_gui.errormsgbox import errorMsgBox
import sys


class MainWindow(QMainWindow):

    kill_thread = pyqtSignal()

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
        self.ui.action_file_new_qemu_instance.triggered.connect(self.showLaunchWizard)
        self.ui.action_file_modify_qemu_instance.triggered.connect(self.selectQemuInstance)
        self.ui.actionModify_Image_Contents.triggered.connect(self.showDiskImageWidget)
        self.ui.action_file_exit.triggered.connect(self.close)
        self.ui.action_help_about.triggered.connect(self.showAboutSplash)

        # Initialize QEMU Instance Table
        self.init_table()

        # Load xterm terminal into the terminal widget
        self.ui.terminalTabWidget.clear()  # clear the default tabs
        self.init_terminalView(0, "Host")

    def init_table(self):
        """initializes table headers"""
        headerData = self.tableModel.headerData(0, Qt.Horizontal)
#        for row in range(0, MAXIMUM_QEMU_INSTANCES):
#            qemuNode = qemuInstance()
#            self.tableModel.insertQemuInstance(qemuNode)
        print(f"header data: {headerData}")
        self.ui.qemuInstanceTable.setModel(self.tableModel)
        self.ui.qemuInstanceTable.setColumnWidth(0, 186)
        self.ui.qemuInstanceTable.setColumnWidth(1, 186)
        self.ui.qemuInstanceTable.setColumnWidth(2, 130)
        self.ui.qemuInstanceTable.setColumnWidth(3, 30)

    def init_terminalView(self, tabIndex, tabName, cmdstr=""):
        """initializes tab view with terminal windows for QEMU instances"""
        term = terminalWidget(self)
        tabSize = self.ui.terminalTabWidget.size()
        term.resize(tabSize)
        term.startXterm(tabName,cmdstr)
        self.ui.terminalTabWidget.insertTab(tabIndex, term, tabName)

    def startQemuTerminal(self,qemu):
        '''starts a terminal to monitor the qemu instance'''
        nextTab = self.ui.terminalTabWidget.count()
        print (f"The current tab position is {nextTab}")
        client = docker.from_env()
        start = time.time()
        elapsed=0
        while elapsed < DOCKER_TIMEOUT:
            containers = client.containers.list()
            print(f"containers at elapsed {elapsed}: {containers}")
            elapsed = (time.time() - start)
            if len(containers) >= nextTab*2: #Hacky way to see if containers started, need to search for name
                #verify correct container started
                time.sleep(1)  #Give container a second to establish
                break
            time.sleep(0.5)

        cmd=f"docker attach {qemu.name.lower()}_xilinx-zcu106_1"
        self.init_terminalView(nextTab,qemu.name,cmd)

    def showLaunchWizard(self, qemuName=""):
        """start qemu instance launch wizard in dock"""
        if self.tableModel.validDataCount() < MAXIMUM_QEMU_INSTANCES:
            launchWiz = QemuLaunchWizard(self)
            launchWiz.newQemuSignal.connect(self.tableModel.insertQemuInstance)
            launchWiz.newQemuSignal.connect(self.startQemuTerminal)
            launchWiz.newDeviceSignal.connect(self.deviceListModel.insertDevice)
            launchWiz.removeDeviceSignal.connect(self.deviceListModel.removeDevice)
            launchWiz.ui.deviceListView.setModel(self.deviceListModel)
            launchWiz.populateFields(qemuName)
            launchWiz.show()

        else:
            print("Error: All QEMU Instances Used")
            errorMsgBox(self, "All QEMU Instances Utilized")

    def selectQemuInstance(self):
        """Shows a selection dialog to pick one of the defined QEMU instances to modify"""
        # Find env files from docker folder
        files = os.listdir(DOCKER_ROOT)
        qemus = []
        #Find all .env files
        for f in files:
            (name, ext) = os.path.splitext(f)
            if ext == ".env" and name:
                qemus.append(name)

        #Create a drop down dialog with qemu names
        (name, ok) = QInputDialog.getItem(self,"Edit QEMU Instance","Select QEMU Instance",qemus,editable=False)

        # Populate wizard with values
        if ok:
            self.showLaunchWizard(qemuName=name)


    def showDiskImageWidget(self):
        '''Displays the widget for interacting iwth the guest disk image file'''
        print("Launching the disk image widget")
        self.diskImageWidget = diskImageWidget()
        self.diskImageWidget.show()


    def showAboutSplash(self):
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
