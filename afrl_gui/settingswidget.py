# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

import subprocess, re
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QPushButton
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLineEdit, QCheckBox, QPlainTextEdit
from afrl_gui.parametersetting import parameterSetting


class settingsWidget(QWidget):

    settingsSignal = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)
        # Scroll Area for form data
        self.formArea = QScrollArea(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.formArea)
        self.form = QWidget()
        self.form.setLayout(QGridLayout())

        # Ok/Cancel buttons for comitting or aborting
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.applySettings)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.window().close)
        okCancel = QWidget(self)
        okCancel.setLayout(QHBoxLayout())
        okCancel.layout().addWidget(okButton)
        okCancel.layout().addWidget(cancelButton)
        self.layout().addWidget(okCancel)

        # Base Class declaration of attributes
        self.paramStr = ""
        self.settings = []
        self.deviceStr = ""
        self.infoDelimiter = ""  # delimiter string between setting name and type/notes
        self.typeStrip = ""  # chars to remove from type strings
        self.notesStrip = ""  # chars to remove from notes strings
        self.headerPattern = re.compile(r"NULL")

    def populateForm(self):
        qemuOut = subprocess.run(["./qemu-system-aarch64", self.paramStr, f"{self.deviceStr},?"], capture_output=True)
        if(qemuOut.returncode != 0):
            print(f"ERROR: qemu-system-aarch64 {self.paramStr} {self.deviceStr},? returned error code: {qemuOut.returncode}")
            return
        outStr = qemuOut.stdout.decode("utf-8")

        # Parse out all the device parameterscandidates
        values = outStr.split('\n')  # Split into lines, process each line
        layoutRow = 0
        self.setWindowTitle(f"{self.deviceStr} Settings")
        self.toggleAllCB = QCheckBox()
        self.toggleAllCB.stateChanged.connect(self.toggleAllRows)
        self.form.layout().addWidget(self.toggleAllCB, layoutRow, 0)

        layoutRow += 1
        for v in values:
            if not v:
                continue  # skip empty strings
            header = self.headerPattern.match(v)
            if header is not None:
                continue  # Skip header
            (label, info) = v.split('=', maxsplit=1)
            labelParts = label.split(f"{self.deviceStr}.",maxsplit=1)
            if len(labelParts) > 1:
                label = labelParts[1].strip()
            else:
                label = labelParts[0].strip()
            info = info.split(self.infoDelimiter)
            type = info[0]
            notes = ""
            if len(info) > 1:
                notes = info[1]
            type = type.strip().strip(self.typeStrip)
            notes = notes.strip().strip(self.notesStrip)
            self.settings.append(parameterSetting(label, type, notes))

        self.settings.sort()
        for s in self.settings:
            settingLabel = QLabel(s.name())
            settingLabel.setAlignment(Qt.AlignRight)
            settingLabel.setToolTip(f"{s.type()}\n{s.notes()}")
            enableSettingCB = QCheckBox()
            enableSettingCB.stateChanged.connect(self.checkSettingsRows)
            self.form.layout().addWidget(enableSettingCB, layoutRow, 0)
            self.form.layout().addWidget(settingLabel, layoutRow, 1)
            if s.type() == 'bool':
                checkBox = QCheckBox()
                checkBox.setEnabled(False)
                self.form.layout().addWidget(checkBox, layoutRow, 2)
            else:
                lineEdit = QLineEdit()
                lineEdit.setEnabled(False)
                self.form.layout().addWidget(lineEdit, layoutRow, 2)
            layoutRow += 1

        #  Add catch all lineedit for additional arguments
        settingLabel = QLabel("Additional Arguments")
        settingLabel.setToolTip("Additional configuration arguments, see qemu-system-aarch64 -help for more information")
        enableSettingCB = QCheckBox()
        enableSettingCB.stateChanged.connect(self.checkSettingsRows)
        self.form.layout().addWidget(enableSettingCB, layoutRow, 0)
        self.form.layout().addWidget(settingLabel, layoutRow, 1)
        self.form.layout().addWidget(QPlainTextEdit(), layoutRow, 2)
        self.formArea.setWidget(self.form)
        self.formArea.show()

    def toggleAllRows(self):
        for r in range(1, self.form.layout().rowCount()):
            self.form.layout().itemAtPosition(r, 0).widget().setChecked(self.toggleAllCB.isChecked())

    def checkSettingsRows(self):
        for r in range(1, self.form.layout().rowCount()):
            if self.form.layout().itemAtPosition(r, 0).widget().isChecked():
                self.form.layout().itemAtPosition(r, 2).widget().setEnabled(True)
            else:
                self.form.layout().itemAtPosition(r, 2).widget().setEnabled(False)

    def applySettings(self):
        '''Apply the settings to the data model '''
        settings = []
        for r in range(1, self.form.layout().rowCount()):
            if self.form.layout().itemAtPosition(r, 0).widget().isChecked():
                arg = self.form.layout().itemAtPosition(r, 1).widget().text()
                widget = self.form.layout().itemAtPosition(r, 2).widget()
                if widget.metaObject().className() == "QCheckBox":
                    settings.append(f"{arg}={str(widget.isChecked()).lower()}")
                if widget.metaObject().className() == "QLineEdit":
                    settings.append(f"{arg}={widget.text()}")
                if widget.metaObject().className() == "QPlainTextEdit":
                    additionalArguments = widget.toPlainText().split('\n')
                    for line in additionalArguments:
                        settings.append(line)
        self.settingsSignal.emit(settings)
        self.window().close()

