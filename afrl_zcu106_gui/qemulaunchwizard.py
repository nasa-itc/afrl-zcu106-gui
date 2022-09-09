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

from PyQt5.QtWidgets import QFileDialog, QWizard, QPlainTextEdit,QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon,QIntValidator

from afrl_zcu106_gui.common import RESOURCE_ROOT, QEMU_IMAGE_FILTERS, QEMU_CFG_FILTERS, NETWORK_CFG
from afrl_zcu106_gui.ui.ui_qemulaunchwizard import Ui_qemuLaunchWizard
from afrl_zcu106_gui.qemuinstance import qemuInstance

from afrl_zcu106_gui.qemudevicelist import qemuDeviceList
from afrl_zcu106_gui.devicesettingswidget import deviceSettingsWidget
from afrl_zcu106_gui.diskimagewidget import diskImageWidget


class QemuLaunchWizard(QWizard):

    kill_signal = pyqtSignal(bool)
    newQemuSignal = pyqtSignal(object)
    newDeviceSignal = pyqtSignal(str, list)  # signal device and list of settings
    removeDeviceSignal = pyqtSignal(list) # removes device at index provided

    def __init__(self, parent):
        super().__init__(parent)
        self.deviceList = qemuDeviceList()  # The list of device candidates to populate dropdown with
        # Intermediate storage for device specific settings
        self.devices = []  # The list of devices configured to launch with the QEMU instance
        self.deviceSettings = []  # A list of device settings lists corresponding to the devices list
        self.init_ui()
        self.lastImageDirectory = "~/"
        self.lastCfgDirectory = "~/"

    def init_ui(self):
        self.ui = Ui_qemuLaunchWizard()
        self.ui.setupUi(self)

        # Setup Buttons
        icon = QIcon()
        icon.addFile(os.path.join(RESOURCE_ROOT, "document-open.png"), QSize(),
                     QIcon.Normal, QIcon.On)
        self.ui.configSelectButton.setIcon(icon)
        self.ui.imageSelectButton.setIcon(icon)
        self.ui.configSelectButton.clicked.connect(self.openCfgFileBrowser)
        self.ui.imageSelectButton.clicked.connect(self.openImageFileBrowser)
        self.ui.modImagePushButton.clicked.connect(self.launchDiskImageWidget)
        self.ui.addDevicePushButton.clicked.connect(self.openDeviceSettings)
        self.ui.removeDevicePushButton.clicked.connect(self.removeDevice)
        self.ui.editDevicePushButton.clicked.connect(self.editDevice)
        self.button(QWizard.FinishButton).clicked.connect(self.launchQemuInstance)


        # Configure the dropdown menus
        self.initDeviceTypeDropdown()

        # Register ui fields
        self.ui.qemuLaunchWizardNamePage.registerField(
            "instanceName*", self.ui.nameLineEdit)
        self.ui.qemuLaunchWizardNamePage.registerField(
            "description", self.ui.descriptionPlainTextEdit, "plainText")
        self.ui.qemuLaunchWizardImagePage.registerField(
            "configFile*", self.ui.configLineEdit)
        self.ui.qemuLaunchWizardImagePage.registerField(
            "image*", self.ui.imageLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "ifaceName*", self.ui.ifaceLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "ipAddress*", self.ui.ipLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "gateway", self.ui.gatewayLineEdit)
        self.ui.qemuLaunchWizardNetworkPage.registerField(
            "subnetMask*", self.ui.subnetMaskLineEdit)

    def openCfgFileBrowser(self):
        (filename, dir) = self.openFileBrowser(
                        "Open Config File", QEMU_CFG_FILTERS, self.lastCfgDirectory)
        self.ui.configLineEdit.setText(filename)
        self.lastCfgDirectory = dir
        print("Setting last kernel directory to " + self.lastCfgDirectory)

    def openImageFileBrowser(self):
        (filename, dir) = self.openFileBrowser(
                            "Open Image File", QEMU_IMAGE_FILTERS, self.lastImageDirectory)
        self.ui.imageLineEdit.setText(filename)
        self.lastImageDirectory = dir

    def launchDiskImageWidget(self):
        '''Displays the widget for interacting iwth the guest disk image file'''
        print(f"Launching the disk image widget to modify {self.ui.imageLineEdit.text()}")
        self.diskImageWidget = diskImageWidget(self,self.ui.imageLineEdit.text())
        self.diskImageWidget.setFloating(True)
        self.diskImageWidget.show()


    def openFileBrowser(self, title="Open File", fileFilters=[], directory=""):
        fd = QFileDialog(self, title)
        fd.setNameFilters(fileFilters)
        fd.setDirectory(directory)
        if(fd.exec_()):
            filename = fd.selectedFiles()[0]  #Single Selection mode, only one file returned in list
            dir = os.path.dirname(filename)
            return (filename, dir)

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

    def applyDeviceSettings(self, settings):
        '''slot to gather and save the device settings strings '''
        device = self.ui.deviceComboBox.currentText()
        self.devices.append(device)
        self.deviceSettings.append(settings)
        self.newDeviceSignal.emit(device, self.deviceSettings)

    def removeDevice(self):
        ''' Removes the selected device from the device list '''
        # TODO? Message Box to ask if user is sure?
        selected = self.ui.deviceListView.selectedIndexes()
        self.removeDeviceSignal.emit(selected)

    def editDevice(self):
        ''' Opens the device settings menu for the selected device from the device list '''

    def launchQemuInstance(self):
        '''Verify QEMU model data and launch instance'''
        qemu = qemuInstance()
        qemu.name = self.ui.qemuLaunchWizardNamePage.field("instanceName")
        qemu.description = self.ui.qemuLaunchWizardNamePage.field("description")
        qemu.devices = self.devices
        qemu.deviceSettings = self.deviceSettings
        qemu.imageName = self.ui.qemuLaunchWizardImagePage.field("image")
        qemu.configFile = self.ui.qemuLaunchWizardImagePage.field("configFile")
        qemu.interfaceName = self.ui.qemuLaunchWizardNetworkPage.field("ifaceName")
        qemu.ipAddress.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("ipAddress"))
        qemu.subnetMask.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("subnetMask"))
        if self.ui.qemuLaunchWizardNetworkPage.field("gateway") != "":
            qemu.gateway.setAddress(self.ui.qemuLaunchWizardNetworkPage.field("gateway"))
        print("Created QEMU Instance: ", repr(qemu))
        self.newQemuSignal.emit(qemu)
