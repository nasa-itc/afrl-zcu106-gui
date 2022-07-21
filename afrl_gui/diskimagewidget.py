# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtWidgets import QDockWidget
from PySide6.QtCore import QFileSystemModel
from afrl_gui.ui.ui_diskimagewidget import Ui_DiskImageWidget

class DiskImageWidget(QDockWidget):

#    kill_signal = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.fileSystemModel = QFileSystemModel()
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_DiskImageWidget()
        self.ui.setupUi(self)
