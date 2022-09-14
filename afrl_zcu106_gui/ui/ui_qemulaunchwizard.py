# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qemulaunchwizard.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_qemuLaunchWizard(object):
    def setupUi(self, qemuLaunchWizard):
        qemuLaunchWizard.setObjectName("qemuLaunchWizard")
        qemuLaunchWizard.resize(397, 415)
        self.qemuLaunchWizardNamePage = QtWidgets.QWizardPage()
        self.qemuLaunchWizardNamePage.setObjectName("qemuLaunchWizardNamePage")
        self.nameLineEdit = QtWidgets.QLineEdit(self.qemuLaunchWizardNamePage)
        self.nameLineEdit.setGeometry(QtCore.QRect(130, 50, 221, 30))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.nameLabel = QtWidgets.QLabel(self.qemuLaunchWizardNamePage)
        self.nameLabel.setGeometry(QtCore.QRect(50, 50, 70, 30))
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.descritionLabel = QtWidgets.QLabel(self.qemuLaunchWizardNamePage)
        self.descritionLabel.setGeometry(QtCore.QRect(29, 100, 91, 30))
        self.descritionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.descritionLabel.setObjectName("descritionLabel")
        self.descriptionPlainTextEdit = QtWidgets.QPlainTextEdit(self.qemuLaunchWizardNamePage)
        self.descriptionPlainTextEdit.setGeometry(QtCore.QRect(130, 110, 221, 131))
        self.descriptionPlainTextEdit.setObjectName("descriptionPlainTextEdit")
        self.deletePushButton = QtWidgets.QPushButton(self.qemuLaunchWizardNamePage)
        self.deletePushButton.setGeometry(QtCore.QRect(130, 260, 89, 25))
        self.deletePushButton.setObjectName("deletePushButton")
        qemuLaunchWizard.addPage(self.qemuLaunchWizardNamePage)
        self.qemuLaunchWizardImagePage = QtWidgets.QWizardPage()
        self.qemuLaunchWizardImagePage.setObjectName("qemuLaunchWizardImagePage")
        self.frame_6 = QtWidgets.QFrame(self.qemuLaunchWizardImagePage)
        self.frame_6.setGeometry(QtCore.QRect(10, 100, 361, 101))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.imageSelectButton = QtWidgets.QPushButton(self.frame_6)
        self.imageSelectButton.setGeometry(QtCore.QRect(320, 10, 30, 30))
        self.imageSelectButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("../resources/document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.imageSelectButton.setIcon(icon)
        self.imageSelectButton.setObjectName("imageSelectButton")
        self.imageLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.imageLineEdit.setGeometry(QtCore.QRect(150, 10, 171, 30))
        self.imageLineEdit.setText("")
        self.imageLineEdit.setObjectName("imageLineEdit")
        self.imageLabel = QtWidgets.QLabel(self.frame_6)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 111, 30))
        self.imageLabel.setObjectName("imageLabel")
        self.modImagePushButton = QtWidgets.QPushButton(self.frame_6)
        self.modImagePushButton.setGeometry(QtCore.QRect(178, 50, 171, 31))
        self.modImagePushButton.setObjectName("modImagePushButton")
        self.frame_8 = QtWidgets.QFrame(self.qemuLaunchWizardImagePage)
        self.frame_8.setGeometry(QtCore.QRect(10, 0, 361, 91))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.configLineEdit = QtWidgets.QLineEdit(self.frame_8)
        self.configLineEdit.setGeometry(QtCore.QRect(150, 20, 171, 30))
        self.configLineEdit.setText("")
        self.configLineEdit.setObjectName("configLineEdit")
        self.configSelectButton = QtWidgets.QPushButton(self.frame_8)
        self.configSelectButton.setGeometry(QtCore.QRect(320, 20, 30, 30))
        self.configSelectButton.setText("")
        self.configSelectButton.setIcon(icon)
        self.configSelectButton.setObjectName("configSelectButton")
        self.configLabel = QtWidgets.QLabel(self.frame_8)
        self.configLabel.setGeometry(QtCore.QRect(10, 20, 141, 30))
        self.configLabel.setObjectName("configLabel")
        qemuLaunchWizard.addPage(self.qemuLaunchWizardImagePage)
        self.qemuLaunchWizardNetworkPage = QtWidgets.QWizardPage()
        self.qemuLaunchWizardNetworkPage.setTitle("")
        self.qemuLaunchWizardNetworkPage.setObjectName("qemuLaunchWizardNetworkPage")
        self.frame_7 = QtWidgets.QFrame(self.qemuLaunchWizardNetworkPage)
        self.frame_7.setGeometry(QtCore.QRect(0, 0, 361, 231))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.ipLineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.ipLineEdit.setGeometry(QtCore.QRect(150, 60, 171, 30))
        self.ipLineEdit.setObjectName("ipLineEdit")
        self.gatewayLabel = QtWidgets.QLabel(self.frame_7)
        self.gatewayLabel.setGeometry(QtCore.QRect(30, 100, 111, 30))
        self.gatewayLabel.setObjectName("gatewayLabel")
        self.ipLabel = QtWidgets.QLabel(self.frame_7)
        self.ipLabel.setGeometry(QtCore.QRect(30, 60, 111, 30))
        self.ipLabel.setObjectName("ipLabel")
        self.subnetMaskLabel = QtWidgets.QLabel(self.frame_7)
        self.subnetMaskLabel.setGeometry(QtCore.QRect(30, 140, 111, 30))
        self.subnetMaskLabel.setObjectName("subnetMaskLabel")
        self.gatewayLineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.gatewayLineEdit.setGeometry(QtCore.QRect(150, 100, 171, 30))
        self.gatewayLineEdit.setObjectName("gatewayLineEdit")
        self.subnetMaskLineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.subnetMaskLineEdit.setGeometry(QtCore.QRect(150, 140, 171, 30))
        self.subnetMaskLineEdit.setObjectName("subnetMaskLineEdit")
        self.ifaceLabel = QtWidgets.QLabel(self.frame_7)
        self.ifaceLabel.setGeometry(QtCore.QRect(30, 20, 111, 30))
        self.ifaceLabel.setObjectName("ifaceLabel")
        self.ifaceLineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.ifaceLineEdit.setGeometry(QtCore.QRect(150, 20, 171, 30))
        self.ifaceLineEdit.setText("")
        self.ifaceLineEdit.setObjectName("ifaceLineEdit")
        qemuLaunchWizard.addPage(self.qemuLaunchWizardNetworkPage)
        self.qemuLaunchWizardDevicePage = QtWidgets.QWizardPage()
        self.qemuLaunchWizardDevicePage.setObjectName("qemuLaunchWizardDevicePage")
        self.frame_3 = QtWidgets.QFrame(self.qemuLaunchWizardDevicePage)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 371, 101))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.deviceTypeLabel = QtWidgets.QLabel(self.frame_3)
        self.deviceTypeLabel.setGeometry(QtCore.QRect(8, 10, 81, 31))
        self.deviceTypeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deviceTypeLabel.setObjectName("deviceTypeLabel")
        self.deviceLabel = QtWidgets.QLabel(self.frame_3)
        self.deviceLabel.setGeometry(QtCore.QRect(38, 50, 51, 31))
        self.deviceLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deviceLabel.setObjectName("deviceLabel")
        self.deviceTypeComboBox = QtWidgets.QComboBox(self.frame_3)
        self.deviceTypeComboBox.setGeometry(QtCore.QRect(100, 10, 191, 31))
        self.deviceTypeComboBox.setObjectName("deviceTypeComboBox")
        self.deviceComboBox = QtWidgets.QComboBox(self.frame_3)
        self.deviceComboBox.setGeometry(QtCore.QRect(100, 50, 191, 31))
        self.deviceComboBox.setObjectName("deviceComboBox")
        self.addDevicePushButton = QtWidgets.QPushButton(self.frame_3)
        self.addDevicePushButton.setGeometry(QtCore.QRect(300, 10, 61, 71))
        self.addDevicePushButton.setObjectName("addDevicePushButton")
        self.frame_4 = QtWidgets.QFrame(self.qemuLaunchWizardDevicePage)
        self.frame_4.setGeometry(QtCore.QRect(0, 110, 371, 241))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.deviceListView = QtWidgets.QListView(self.frame_4)
        self.deviceListView.setGeometry(QtCore.QRect(0, 0, 291, 231))
        self.deviceListView.setObjectName("deviceListView")
        self.removeDevicePushButton = QtWidgets.QPushButton(self.frame_4)
        self.removeDevicePushButton.setGeometry(QtCore.QRect(300, 80, 61, 61))
        self.removeDevicePushButton.setObjectName("removeDevicePushButton")
        self.editDevicePushButton = QtWidgets.QPushButton(self.frame_4)
        self.editDevicePushButton.setGeometry(QtCore.QRect(300, 10, 61, 61))
        self.editDevicePushButton.setObjectName("editDevicePushButton")
        qemuLaunchWizard.addPage(self.qemuLaunchWizardDevicePage)

        self.retranslateUi(qemuLaunchWizard)
        QtCore.QMetaObject.connectSlotsByName(qemuLaunchWizard)

    def retranslateUi(self, qemuLaunchWizard):
        _translate = QtCore.QCoreApplication.translate
        qemuLaunchWizard.setWindowTitle(_translate("qemuLaunchWizard", "QEMU Configuration Wizard"))
        self.nameLabel.setText(_translate("qemuLaunchWizard", "Name"))
        self.descritionLabel.setText(_translate("qemuLaunchWizard", "Description"))
        self.deletePushButton.setText(_translate("qemuLaunchWizard", "Delete"))
        self.imageLabel.setText(_translate("qemuLaunchWizard", "Image File"))
        self.modImagePushButton.setText(_translate("qemuLaunchWizard", "Modify Image Contents"))
        self.configLabel.setText(_translate("qemuLaunchWizard", "Config File"))
        self.ipLineEdit.setText(_translate("qemuLaunchWizard", "000.000.000.000"))
        self.gatewayLabel.setText(_translate("qemuLaunchWizard", "Gateway"))
        self.ipLabel.setText(_translate("qemuLaunchWizard", "IP Address"))
        self.subnetMaskLabel.setText(_translate("qemuLaunchWizard", "Subnet Mask"))
        self.gatewayLineEdit.setText(_translate("qemuLaunchWizard", "000.000.000.000"))
        self.subnetMaskLineEdit.setText(_translate("qemuLaunchWizard", "000.000.000.000"))
        self.ifaceLabel.setText(_translate("qemuLaunchWizard", "Interface Name"))
        self.deviceTypeLabel.setText(_translate("qemuLaunchWizard", "Device Type"))
        self.deviceLabel.setText(_translate("qemuLaunchWizard", "Device"))
        self.addDevicePushButton.setText(_translate("qemuLaunchWizard", "Add"))
        self.removeDevicePushButton.setText(_translate("qemuLaunchWizard", "Remove"))
        self.editDevicePushButton.setText(_translate("qemuLaunchWizard", "Edit"))
