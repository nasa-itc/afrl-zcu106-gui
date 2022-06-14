# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
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

import os.path

from PySide6.QtWidgets import QFileDialog, QWizard
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon

from afrl_gui.common import RESOURCE_ROOT
from afrl_gui.ui.ui_qemulaunchwizard import Ui_qemuLaunchWizard
from afrl_gui.qemuinstance import qemuInstance

from afrl_gui.qemumachinelist import qemuMachineList
from afrl_gui.qemucpulist import qemuCpuList
from afrl_gui.qemudevicelist import qemuDeviceList
from afrl_gui.devicesettingswidget import deviceSettingsWidget
from afrl_gui.machinesettingswidget import machineSettingsWidget

lastKernelDirectory = "/home/afrl_dev"
lastAppDirectory = "/home/afrl_dev"


class QemuLaunchWizard(QWizard):

    kill_signal = Signal(bool)
    newQemuSignal = Signal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.machineList = qemuMachineList()
        self.cpuList = qemuCpuList()
        self.deviceList = qemuDeviceList()
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_qemuLaunchWizard()
        self.ui.setupUi(self)

        # Setup Buttons
        icon = QIcon()
        icon.addFile(os.path.join(RESOURCE_ROOT, "document-open.png"), QSize(),
                     QIcon.Normal, QIcon.On)
        self.ui.kernelButton.setIcon(icon)
        self.ui.appButton.setIcon(icon)
        self.ui.kernelButton.clicked.connect(self.openKernelFileBrowser)
        self.ui.appButton.clicked.connect(self.openAppFileBrowser)
        self.ui.boardSettings_PushButton.clicked.connect(self.openMachineSettings)
        self.ui.deviceSettingsButton.clicked.connect(self.openDeviceSettings)
        self.button(QWizard.FinishButton).clicked.connect(self.launchQemuInstance)

        # Populate the dropdown menus
        self.initMachineDropdown()
        self.initCpuDropdown()
        self.initDeviceTypeDropdown()

        # Register ui fields
        self.ui.qemuLaunchWizardNamePage.registerField(
            "instanceName*", self.ui.nameLineEdit)
        self.ui.qemuLaunchWizardMachineCpuPage.registerField(
            "machine", self.ui.machineComboBox)
        self.ui.qemuLaunchWizardMachineCpuPage.registerField(
            "cpu", self.ui.cpuComboBox)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "ipAddress*", self.ui.ipLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "subnetMask*", self.ui.subnetMaskLineEdit)
        self.ui.qemuLaunchWizardKernelAppPage.registerField(
            "kernel*", self.ui.kernelLineEdit)
        self.ui.qemuLaunchWizardKernelAppPage.registerField(
            "application*", self.ui.appLineEdit)

    def openKernelFileBrowser(self):
        (filename, dir) = self.openFileBrowser(
                        "Open Kernel File", lastKernelDirectory, "*.bin")
        self.ui.kernelLineEdit.setText(filename)
        self.lastKernelDirectory = dir
        print("Setting last kernel directory to " + self.lastKernelDirectory)

    def openAppFileBrowser(self):
        (filename, dir) = self.openFileBrowser(
                        "Open Application File", lastAppDirectory, "*")
        self.ui.appLineEdit.setText(filename)
        self.lastAppDirectory = dir
        print("Setting last kernel directory to " + self.lastKernelDirectory)

    def openFileBrowser(self, title, fileFilter, directory):
        (filename, filter) = QFileDialog.getOpenFileName(
                                         self, title, fileFilter, directory)
        dir = os.path.dirname(filename)
        return (filename, dir)

    def initMachineDropdown(self):
        for idx in range(0, len(self.machineList)):
            self.ui.machineComboBox.addItem(self.machineList[idx].argument())
            self.ui.machineComboBox.setItemData(idx, self.machineList[idx].description(), role=Qt.ToolTipRole)

    def initCpuDropdown(self):
        self.ui.cpuComboBox.addItems(self.cpuList.argumentList())
        self.ui.cpuComboBox.activated.connect(self.selectCpu)

    def selectCpu(self, idx):
        print(f"Selected CPU is: {self.cpuList[idx].argument()}")

    def initDeviceTypeDropdown(self):
        self.ui.deviceTypeComboBox.addItems(self.deviceList.deviceTypeList())
        self.ui.deviceTypeComboBox.activated.connect(self.populateDeviceDropdown)
        self.populateDeviceDropdown(0)

    def populateDeviceDropdown(self, typeIdx):
        deviceList = self.deviceList.deviceLists()[typeIdx]
        self.ui.deviceComboBox.clear()
        for idx in range(0, len(deviceList)):
            self.ui.deviceComboBox.addItem(deviceList[idx].argument())
            self.ui.deviceComboBox.setItemData(idx,deviceList[idx].toolTipText(), role=Qt.ToolTipRole)

    def openDeviceSettings(self):
        '''Populates a form for configuring device settings '''
        deviceStr = self.ui.deviceComboBox.currentText()
        self.deviceSettingsWidget = deviceSettingsWidget(self, deviceStr)
        self.deviceSettingsWidget.show()

    def openMachineSettings(self):
        '''Populates a form for configuring device settings '''
        machineStr = self.ui.machineComboBox.currentText()
        self.machineSettingsWidget = machineSettingsWidget(self, machineStr)
        self.machineSettingsWidget.show()

    def launchQemuInstance(self):
        '''Verify QEMU model data and launch instance'''
        qemu = qemuInstance()
        qemu.name = self.ui.qemuLaunchWizardNamePage.field("instanceName")
        qemu.machine = self.machineList[self.ui.qemuLaunchWizardMachineCpuPage.field("machine")].argument()
        qemu.cpu = self.cpuList[self.ui.qemuLaunchWizardMachineCpuPage.field("cpu")].argument()
        qemu.ipAddress.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("ipAddress"))
        qemu.subnetMask.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("subnetMask"))
        qemu.kernel = self.ui.qemuLaunchWizardKernelAppPage.field("kernel")
        qemu.application = self.ui.qemuLaunchWizardKernelAppPage.field("application")
        print("Created QEMU Instance: ", repr(qemu))
        self.newQemuSignal.emit(qemu)
