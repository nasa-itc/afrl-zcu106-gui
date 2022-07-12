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

from PySide6.QtWidgets import QFileDialog, QWizard, QPlainTextEdit
from PySide6.QtCore import Qt, Signal, Slot, QSize
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
    newDeviceSignal = Signal(str, list)  # signal device and list of settings

    def __init__(self, parent):
        super().__init__(parent)
        self.machineList = qemuMachineList()  # The list of machine candidates to populate dropdown with
        self.cpuList = qemuCpuList()  # The list of cpu candidates to populate dropdown with
        self.deviceList = qemuDeviceList()  # The list of device candidates to populate dropdown with
        # Intermediate storage for device and machine specific settings
        self.machineSettings = []
        self.devices = []  # The list of devices configured to launch with the QEMU instance
        self.deviceSettings = []  # A list of device settings lists corresponding to the devices list
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
        self.ui.addDevicePushButton.clicked.connect(self.openDeviceSettings)
        self.button(QWizard.FinishButton).clicked.connect(self.launchQemuInstance)

        # Populate the dropdown menus
        self.initMachineDropdown()
        self.initCpuDropdown()
        self.initDeviceTypeDropdown()
        # Monitor machine selection to disable CPU selection if machine is selected
        self.ui.machineComboBox.currentTextChanged.connect(self.setCpuSelectionStatus)

        # Register ui fields
        self.ui.qemuLaunchWizardNamePage.registerField(
            "instanceName*", self.ui.nameLineEdit)
        self.ui.qemuLaunchWizardNamePage.registerField(
            "description", self.ui.descriptionPlainTextEdit, "plainText")
        self.ui.qemuLaunchWizardMachineCpuPage.registerField(
            "machine", self.ui.machineComboBox)
        self.ui.qemuLaunchWizardMachineCpuPage.registerField(
            "cpu", self.ui.cpuComboBox)
        self.ui.qemuLaunchWizardMachineCpuPage.registerField(
            "memory", self.ui.memorySpinBox)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "ipAddress*", self.ui.ipLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "subnetMask*", self.ui.subnetMaskLineEdit)
        self.ui.qemuLaunchWizardKernelAppPage.registerField(
            "kernel*", self.ui.kernelLineEdit)
        self.ui.qemuLaunchWizardKernelAppPage.registerField(
            "application*", self.ui.appLineEdit)

        # Setup the memory entry widget to only produce values with power of 2
        self.lastMemoryValue = self.ui.memorySpinBox.value()
        self.ui.memorySpinBox.valueChanged.connect(self.adjustMemoryValue)
        self.ui.memorySpinBox.lineEdit().setReadOnly(True)

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
            self.ui.deviceComboBox.setItemData(idx, deviceList[idx].toolTipText(), role=Qt.ToolTipRole)

    def openDeviceSettings(self):
        '''Populates a form for configuring device settings '''
        deviceStr = self.ui.deviceComboBox.currentText()
        self.deviceSettingsWidget = deviceSettingsWidget(deviceStr)
        self.deviceSettingsWidget.settingsSignal.connect(self.applyDeviceSettings)
        self.deviceSettingsWidget.show()

    @Slot(list)
    def applyDeviceSettings(self, settings):
        '''slot to gather and save the device settings strings '''
        print(f"DEVICE SETTINGS: {settings}")
        device = self.ui.deviceComboBox.currentText()
        self.devices.append(device)
        self.deviceSettings.append(settings)
        self.newDeviceSignal.emit(device, self.deviceSettings)

    def openMachineSettings(self):
        '''Populates a form for configuring device settings '''
        machineStr = self.ui.machineComboBox.currentText()
        self.machineSettingsWidget = machineSettingsWidget(machineStr)
        self.machineSettingsWidget.settingsSignal.connect(self.applyMachineSettings)
        self.machineSettingsWidget.show()

    @Slot(list)
    def applyMachineSettings(self, settings):
        '''slot to gather and save the machine settings strings '''
        print(f"MACHINE SETTINGS: {settings}")
        self.machineSettings = settings

    @Slot(str)
    def setCpuSelectionStatus(self, text):
        if text != "":
            self.ui.cpuComboBox.setEnabled(False)
            self.ui.cpuComboBox.setCurrentIndex(0)  # Clear out any CPU setting, idx 0 is default/empty
            self.ui.cpuSettings_PushButton.setEnabled(False)
        else:
            self.ui.cpuComboBox.setEnabled(True)
            self.ui.cpuSettings_PushButton.setEnabled(True)

    @Slot(int)
    def adjustMemoryValue(self, value):
        '''slot to adjust the memory value to a power of 2 on change'''
        print(f"Memory Changing, recieved value {value}")
        if value > self.lastMemoryValue:
            self.ui.memorySpinBox.setValue(self.lastMemoryValue * 2)
        else:
            self.ui.memorySpinBox.setValue(self.lastMemoryValue / 2)
        self.lastMemoryValue = self.ui.memorySpinBox.value()

    def launchQemuInstance(self):
        '''Verify QEMU model data and launch instance'''
        qemu = qemuInstance()
        qemu.name = self.ui.qemuLaunchWizardNamePage.field("instanceName")
        qemu.description = self.ui.qemuLaunchWizardNamePage.field("description")
        qemu.machine = self.machineList[self.ui.qemuLaunchWizardMachineCpuPage.field("machine")].argument()
        qemu.machineSettings = self.machineSettings
        qemu.cpu = self.cpuList[self.ui.qemuLaunchWizardMachineCpuPage.field("cpu")].argument()
        qemu.memory = self.ui.qemuLaunchWizardMachineCpuPage.field("memory")
        qemu.devices = self.devices
        qemu.deviceSettings = self.deviceSettings
        qemu.ipAddress.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("ipAddress"))
        qemu.subnetMask.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("subnetMask"))
        qemu.kernel = self.ui.qemuLaunchWizardKernelAppPage.field("kernel")
        qemu.application = self.ui.qemuLaunchWizardKernelAppPage.field("application")
        print("Created QEMU Instance: ", repr(qemu))
        self.newQemuSignal.emit(qemu)
