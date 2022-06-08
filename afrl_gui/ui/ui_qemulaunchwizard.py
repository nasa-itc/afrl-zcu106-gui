# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qemulaunchwizard.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QWizard,
    QWizardPage)

class Ui_qemuLaunchWizard(object):
    def setupUi(self, qemuLaunchWizard):
        if not qemuLaunchWizard.objectName():
            qemuLaunchWizard.setObjectName(u"qemuLaunchWizard")
        qemuLaunchWizard.resize(384, 336)
        self.qemuLaunchWizardNamePage = QWizardPage()
        self.qemuLaunchWizardNamePage.setObjectName(u"qemuLaunchWizardNamePage")
        self.nameLineEdit = QLineEdit(self.qemuLaunchWizardNamePage)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QRect(130, 90, 171, 30))
        self.nameLabel = QLabel(self.qemuLaunchWizardNamePage)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setGeometry(QRect(50, 90, 70, 30))
        qemuLaunchWizard.addPage(self.qemuLaunchWizardNamePage)
        self.qemuLaunchWizardMachineCpuPage = QWizardPage()
        self.qemuLaunchWizardMachineCpuPage.setObjectName(u"qemuLaunchWizardMachineCpuPage")
        self.machineComboBox = QComboBox(self.qemuLaunchWizardMachineCpuPage)
        self.machineComboBox.setObjectName(u"machineComboBox")
        self.machineComboBox.setGeometry(QRect(130, 40, 191, 31))
        self.label = QLabel(self.qemuLaunchWizardMachineCpuPage)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 40, 81, 31))
        self.boardSettings_PushButton = QPushButton(self.qemuLaunchWizardMachineCpuPage)
        self.boardSettings_PushButton.setObjectName(u"boardSettings_PushButton")
        self.boardSettings_PushButton.setGeometry(QRect(168, 80, 151, 31))
        self.cpuSettings_PushButton = QPushButton(self.qemuLaunchWizardMachineCpuPage)
        self.cpuSettings_PushButton.setObjectName(u"cpuSettings_PushButton")
        self.cpuSettings_PushButton.setGeometry(QRect(168, 170, 151, 31))
        self.cpuComboBox = QComboBox(self.qemuLaunchWizardMachineCpuPage)
        self.cpuComboBox.setObjectName(u"cpuComboBox")
        self.cpuComboBox.setGeometry(QRect(130, 130, 191, 31))
        self.label_2 = QLabel(self.qemuLaunchWizardMachineCpuPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 130, 81, 31))
        qemuLaunchWizard.addPage(self.qemuLaunchWizardMachineCpuPage)
        self.qemuLaunchWizardDevicePage = QWizardPage()
        self.qemuLaunchWizardDevicePage.setObjectName(u"qemuLaunchWizardDevicePage")
        self.deviceComboBox = QComboBox(self.qemuLaunchWizardDevicePage)
        self.deviceComboBox.setObjectName(u"deviceComboBox")
        self.deviceComboBox.setGeometry(QRect(142, 140, 191, 31))
        self.deviceTypeLabel = QLabel(self.qemuLaunchWizardDevicePage)
        self.deviceTypeLabel.setObjectName(u"deviceTypeLabel")
        self.deviceTypeLabel.setGeometry(QRect(50, 50, 81, 31))
        self.deviceLabel = QLabel(self.qemuLaunchWizardDevicePage)
        self.deviceLabel.setObjectName(u"deviceLabel")
        self.deviceLabel.setGeometry(QRect(80, 140, 51, 31))
        self.deviceTypeComboBox = QComboBox(self.qemuLaunchWizardDevicePage)
        self.deviceTypeComboBox.setObjectName(u"deviceTypeComboBox")
        self.deviceTypeComboBox.setGeometry(QRect(142, 50, 191, 31))
        self.deviceSettingsButton = QPushButton(self.qemuLaunchWizardDevicePage)
        self.deviceSettingsButton.setObjectName(u"deviceSettingsButton")
        self.deviceSettingsButton.setGeometry(QRect(180, 180, 151, 31))
        qemuLaunchWizard.addPage(self.qemuLaunchWizardDevicePage)
        self.qemuLaunchWizardNetworkPage = QWizardPage()
        self.qemuLaunchWizardNetworkPage.setObjectName(u"qemuLaunchWizardNetworkPage")
        self.ipLineEdit = QLineEdit(self.qemuLaunchWizardNetworkPage)
        self.ipLineEdit.setObjectName(u"ipLineEdit")
        self.ipLineEdit.setGeometry(QRect(130, 50, 171, 30))
        self.ipLabel = QLabel(self.qemuLaunchWizardNetworkPage)
        self.ipLabel.setObjectName(u"ipLabel")
        self.ipLabel.setGeometry(QRect(10, 50, 111, 30))
        self.subnetMaskLabel = QLabel(self.qemuLaunchWizardNetworkPage)
        self.subnetMaskLabel.setObjectName(u"subnetMaskLabel")
        self.subnetMaskLabel.setGeometry(QRect(10, 90, 111, 30))
        self.subnetMaskLineEdit = QLineEdit(self.qemuLaunchWizardNetworkPage)
        self.subnetMaskLineEdit.setObjectName(u"subnetMaskLineEdit")
        self.subnetMaskLineEdit.setGeometry(QRect(130, 90, 171, 30))
        qemuLaunchWizard.addPage(self.qemuLaunchWizardNetworkPage)
        self.qemuLaunchWizardKernelAppPage = QWizardPage()
        self.qemuLaunchWizardKernelAppPage.setObjectName(u"qemuLaunchWizardKernelAppPage")
        self.appButton = QPushButton(self.qemuLaunchWizardKernelAppPage)
        self.appButton.setObjectName(u"appButton")
        self.appButton.setGeometry(QRect(310, 60, 30, 30))
        icon = QIcon()
        icon.addFile(u"../resources/document-open.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u"../resources/document-open.png", QSize(), QIcon.Normal, QIcon.On)
        self.appButton.setIcon(icon)
        self.appLineEdit = QLineEdit(self.qemuLaunchWizardKernelAppPage)
        self.appLineEdit.setObjectName(u"appLineEdit")
        self.appLineEdit.setGeometry(QRect(141, 60, 171, 30))
        self.kernelLineEdit = QLineEdit(self.qemuLaunchWizardKernelAppPage)
        self.kernelLineEdit.setObjectName(u"kernelLineEdit")
        self.kernelLineEdit.setGeometry(QRect(140, 20, 171, 30))
        self.kernelLabel = QLabel(self.qemuLaunchWizardKernelAppPage)
        self.kernelLabel.setObjectName(u"kernelLabel")
        self.kernelLabel.setGeometry(QRect(19, 20, 111, 30))
        self.appLabel = QLabel(self.qemuLaunchWizardKernelAppPage)
        self.appLabel.setObjectName(u"appLabel")
        self.appLabel.setGeometry(QRect(20, 60, 111, 30))
        self.kernelButton = QPushButton(self.qemuLaunchWizardKernelAppPage)
        self.kernelButton.setObjectName(u"kernelButton")
        self.kernelButton.setGeometry(QRect(310, 20, 30, 30))
        self.kernelButton.setIcon(icon)
        qemuLaunchWizard.addPage(self.qemuLaunchWizardKernelAppPage)

        self.retranslateUi(qemuLaunchWizard)

        QMetaObject.connectSlotsByName(qemuLaunchWizard)
    # setupUi

    def retranslateUi(self, qemuLaunchWizard):
        qemuLaunchWizard.setWindowTitle(QCoreApplication.translate("qemuLaunchWizard", u"Wizard", None))
        self.nameLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Name", None))
        self.label.setText(QCoreApplication.translate("qemuLaunchWizard", u"Board", None))
        self.boardSettings_PushButton.setText(QCoreApplication.translate("qemuLaunchWizard", u"Advanced Settings", None))
        self.cpuSettings_PushButton.setText(QCoreApplication.translate("qemuLaunchWizard", u"Advanced Settings", None))
        self.label_2.setText(QCoreApplication.translate("qemuLaunchWizard", u"CPU", None))
        self.deviceTypeLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Device Type", None))
        self.deviceLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Device", None))
        self.deviceSettingsButton.setText(QCoreApplication.translate("qemuLaunchWizard", u"Advanced", None))
        self.ipLineEdit.setText(QCoreApplication.translate("qemuLaunchWizard", u"000.000.000.000", None))
        self.ipLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"IP Address", None))
        self.subnetMaskLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Subnet Mask", None))
        self.subnetMaskLineEdit.setText(QCoreApplication.translate("qemuLaunchWizard", u"000.000.000.000", None))
        self.appButton.setText("")
        self.appLineEdit.setText(QCoreApplication.translate("qemuLaunchWizard", u"application", None))
        self.kernelLineEdit.setText(QCoreApplication.translate("qemuLaunchWizard", u"kernel", None))
        self.kernelLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Kernel", None))
        self.appLabel.setText(QCoreApplication.translate("qemuLaunchWizard", u"Application", None))
        self.kernelButton.setText("")
    # retranslateUi

