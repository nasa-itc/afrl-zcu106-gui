# This Python file uses the following encoding: utf-8

import time
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

#TODO: Close but not quite, going to have to make custom widget, this blocks until user hits ok
class diskMsgBox(QDialog):
    def __init__(self, imgName="", parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.timeout = 180  # timeout in seconds for mounting image
        self.workingStrs = ['', '.', '..', '...']
        #self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle("Image File Mounting")
        self.setLayout(QGridLayout())
        self.loadingStr = f"{imgName} Loading"
        self.loadingLabel = QLabel(self.loadingStr, self)
        self.layout().addWidget(self.loadingLabel,1,1,1,2,Qt.AlignCenter)
        okButton = QPushButton("OK", self)
        self.layout().addWidget(okButton,2,1,1,1,Qt.AlignCenter)
        cancelButton = QPushButton("Cancel", self)
        self.layout().addWidget(cancelButton,2,2,1,1,Qt.AlignCenter)

    def updateLoadingLabel(self):
        t = self.timeout
        idx = 0
        while t > 0:
            self.loadingLabel.setText(self.loadingStr + self.workingStrs[idx % 3])
            time.sleep(2)
            t -= 2
