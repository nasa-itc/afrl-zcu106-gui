# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import subprocess, re
from PySide6.QtWidgets import QDockWidget, QFileSystemModel, QFileDialog
from afrl_gui.ui.ui_diskimagewidget import Ui_DiskImageWidget
from afrl_gui.errormsgbox import errorMsgBox

class diskImageWidget(QDockWidget):

#    kill_signal = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.hostFileSystemModel = QFileSystemModel()
        # TODO: Pick appropriate entry point for file system views, maybe store last for convenience?
        self.hostFileSystemModel.setRootPath("~/")
        self.guestFileSystemModel = QFileSystemModel()
        self.guestFileSystemModel.setRootPath("~/")
        self.init_ui()

    def init_ui(self):
        self.ui = Ui_DiskImageWidget()
        self.ui.setupUi(self)
        self.ui.hostTreeView.setModel(self.hostFileSystemModel)
        self.ui.hostTreeView.setRootIndex(self.hostFileSystemModel.index("~/"));
        self.ui.guestTreeView.setModel(self.guestFileSystemModel)
        self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index("~/"));
        # Initialize comboboxes with Browse option, need to consider last few locations or default locations as well
        self.ui.hostComboBox.addItem("Browse")
        self.ui.guestComboBox.addItem("Browse")
        self.ui.hostComboBox.textActivated.connect(self.loadHostDirectory)

    def loadHostDirectory(self, path):
        '''Loads the directory at path into the hostTreeView'''
        if path == "Browse":
            fd = QFileDialog(self,"Open Host Directory")
            fd.setFileMode(QFileDialog.Directory)
            fd.setOption(QFileDialog.ShowDirsOnly, True)
            if(fd.exec()):
                dirname = fd.selectedFiles()
                path = dirname[0]
        self.ui.hostTreeView.setRootIndex(self.hostFileSystemModel.index(path))

    def mountImageFile(self, path):
        '''Mounts the disk image file at the input path and displays contents in guestTreeView'''
        diskOut = subprocess.run(["udisksctl", "loop-setup", "-f", path], capture_output=True)
        if(diskOut.returncode != 0):
            errorMsgBox(self, f"Cannot Mount Image at: {path}")
            return
        outStr = diskOut.stdout.decode("utf-8")
