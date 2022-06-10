# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

import subprocess, re
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit


class deviceSetting:
    def __init__(self, name="", type="", notes=""):
        self.__name = name
        self.__type = type
        self.__notes = notes

    def name(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def type(self):
        return self.__type

    def setType(self, type):
        self.__type = type

    def notes(self):
        return self.__notes

    def setNotes(self, notes):
        self.__notes = notes


class deviceSettingsWidget(QWidget):
    def __init__(self, parent, deviceStr):
        super().__init__()
        layout = QGridLayout()
        self.deviceStr = deviceStr
        self.setLayout(layout)
        self.populateForm()

    def populateForm(self):
        qemuOut = subprocess.run(["./qemu-system-aarch64", "-device", f"{self.deviceStr},?"], capture_output=True)
        if(qemuOut.returncode != 0):
            print(f"ERROR: qemu-system-aarch64 -device ? returned error code: {qemuOut.returncode}")
            return
        outStr = qemuOut.stdout.decode("utf-8")

        # Parse out all the device parameterscandidates
        headerPattern = re.compile(r".+ options:")
        values = outStr.split('\n')  # Split into lines, process each line
        layoutRow = 0
        self.layout().addWidget(QLabel("Device"),layoutRow,0)
        self.layout().addWidget(QLabel(f"{self.deviceStr}"),layoutRow,1)
        layoutRow += 1

        for v in values:
            if not v:
                continue # skip empty strings
            print(v)
            header = headerPattern.match(v)
            if header is not None:
                continue  # Skip header
            (label, info) = v.split('=', maxsplit=1)
            label = label.strip()
            info = info.split(' - ')
            type = info[0]
            if len(info) > 1:
                notes = info[1]
            type = type.strip().strip('<>')
            notes = notes.strip()
            self.layout().addWidget(QLabel(label), layoutRow, 0)
            lineEdit = QLineEdit()
            lineEdit.setToolTip(f"{type}\n{notes}")
            self.layout().addWidget(lineEdit, layoutRow, 1)
            layoutRow += 1



