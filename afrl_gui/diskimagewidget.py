# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import subprocess, re, time, os, shutil
from PySide6.QtWidgets import QDockWidget, QFileSystemModel, QFileDialog, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize, Qt
from afrl_gui.ui.ui_diskimagewidget import Ui_DiskImageWidget
from afrl_gui.errormsgbox import errorMsgBox
from afrl_gui.common import QEMU_IMAGE_FILTERS, RESOURCE_ROOT


class diskImageWidget(QDockWidget):

#    kill_signal = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.hostFileSystemModel = QFileSystemModel()
        # TODO: Pick appropriate entry point for file system views, maybe store last for convenience?
        self.hostFileSystemModel.setRootPath("~/")
        self.guestFileSystemModel = QFileSystemModel()
        self.guestFileSystemModel.setRootPath("~/")
        self.guestPath=""
        self.init_ui()

    def __del__(self):
        self.unmountDiskImage()

    def closeEvent(self, event):
        self.unmountDiskImage()


    def init_ui(self):
        self.ui = Ui_DiskImageWidget()
        self.ui.setupUi(self)
        self.ui.hostTreeView.setModel(self.hostFileSystemModel)
        self.ui.hostTreeView.setRootIndex(self.hostFileSystemModel.index("~/"));
        self.ui.guestTreeView.setModel(self.guestFileSystemModel)
        self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index("~/"));
        self.ui.guestTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.guestTreeView.customContextMenuRequested.connect(self.showFileContextMenu)

        # Initialize comboboxes with Browse option, need to consider last few locations or default locations as well
        self.ui.hostComboBox.addItem("Browse")
        self.ui.guestComboBox.addItem("Browse")
        self.ui.hostComboBox.textActivated.connect(self.loadHostDirectory)
        self.ui.guestComboBox.textActivated.connect(self.loadGuestImage)
        rhIcon = QIcon()
        rhIcon.addFile(os.path.join(RESOURCE_ROOT, "rhArrow.svg"), QSize(32,32),
                     QIcon.Normal, QIcon.On)
        self.ui.toGuestPushButton.setIcon(rhIcon)
        self.ui.toGuestPushButton.setIconSize(QSize(32,32))
        self.ui.toGuestPushButton.clicked.connect(self.copyToGuest)
        lhIcon = QIcon()
        lhIcon.addFile(os.path.join(RESOURCE_ROOT, "lhArrow.svg"), QSize(32,32),
                     QIcon.Normal, QIcon.On)
        self.ui.toHostPushButton.setIcon(lhIcon)
        self.ui.toHostPushButton.setIconSize(QSize(32,32))
        self.ui.toHostPushButton.clicked.connect(self.copyToHost)

    def loadHostDirectory(self, path):
        '''Loads the directory at path into the hostTreeView'''
        if path == "Browse":
            fd = QFileDialog(self,"Open Host Directory")
            fd.setFileMode(QFileDialog.Directory)
            fd.setOption(QFileDialog.ShowDirsOnly, True)
            if(fd.exec()):
                dirname = fd.selectedFiles()
                path = dirname[0]
        self.hostFileSystemModel.setRootPath(path)
        self.ui.hostTreeView.setRootIndex(self.hostFileSystemModel.index(path))

    def loadGuestImage(self, path):
        '''Mounts and loads the image file at path into the guestTreeView'''
        if path == "Browse":
            fd = QFileDialog(self, "Open Guest Image")
            fd.setNameFilters(QEMU_IMAGE_FILTERS)
            if(fd.exec()):
                filename = fd.selectedFiles()
                path = filename[0]
                path = self.openImageFile(path)
                self.ui.guestComboBox.setCurrentIndex(0)  # Load the fi
        if path != "":
            self.guestFileSystemModel.setRootPath(path)
            self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(path))

    def openImageFile(self, path):
        '''Opens image file with libguestfs and mounts the partition(s) '''
        self.guestPath = f"{os.path.realpath(os.curdir)}/guestMnt"
        diskOut = subprocess.run(["mkdir", "-p", self.guestPath], capture_output=True)
        diskOut = subprocess.run(["guestmount", "-a", path, "-i", self.guestPath, "-o", f"uid={os.getuid()}", "-o", f"uid={os.getgid()}"], capture_output=True)
        if(diskOut.returncode != 0):
            errorMsgBox(self, f"Cannot Mount Image at: {path}")
            self.guestPath=""  # Clear the path so we don't try to unmount later
            return ""

        # add the mountPAths to the dropdown menu
        self.ui.guestComboBox.insertItems(0,self.guestPath)
        print(f"Mounting complete, mounted drives: {self.guestPath}")
        return self.guestPath # Return first mounted path on success

    def showFileContextMenu(self, position):
        '''displays context menu for file items in the treeviews '''
        editAction = QAction("Edit")
        editAction.triggered.connect(self.editSelection)
        menu = QMenu(self.ui.guestTreeView)
        menu.addAction(editAction)

        menu.exec_(self.ui.guestTreeView.mapToGlobal(position))

    def editSelection(self):
        print("editing selection")

    def copyToGuest(self):
        '''copies file highlighted in host view to guest'''
        sourceSelections = self.ui.hostTreeView.selectedIndexes()
        destSelections = self.ui.guestTreeView.selectedIndexes()
        srcRow = -1
        destRow = -1
        for s in sourceSelections:
            if s.row() == srcRow:
                continue
            src = self.hostFileSystemModel.filePath(s)
            srcRow = s.row()
            for d in destSelections:
                if d.row == destRow:
                    continue
                dest = self.guestFileSystemModel.filePath(d)
            print(f"Host to Guest: Copying {src} to {dest}")
            self.copyFile(src, dest)

    def copyToHost(self):
        '''copies file highlighted in guest view to host'''
        sourceSelections = self.ui.guestTreeView.selectedIndexes()
        destSelections = self.ui.hostTreeView.selectedIndexes()
        srcRow = -1
        destRow = -1
        for s in sourceSelections:
            if s.row() == srcRow:
                continue
            src = self.guestFileSystemModel.filePath(s)
            srcRow = s.row()
            for d in destSelections:
                if d.row == destRow:
                    continue
                dest = self.hostFileSystemModel.filePath(d)
            print(f"Guest to Host: Copying {src} to {dest}")
            self.copyFile(src, dest)

    def copyFile(self, src, dest):
        '''copies a file at src to dest'''
        shutil.copy2(src, dest)

    def unmountDiskImage(self):
        ''' Unmount the guest FS'''
        if self.guestPath != "":
            mountOut = subprocess.run(["guestunmount", self.guestPath], capture_output=True)
            outStr = mountOut.stdout.decode("utf-8")
            print(f"Unmount output: {outStr}")
