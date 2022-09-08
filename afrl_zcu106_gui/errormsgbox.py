# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QMessageBox


class errorMsgBox(QMessageBox):
    def __init__(self, parent, errMsg=""):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle("Error")
        self.setText(errMsg)
        self.exec_()
