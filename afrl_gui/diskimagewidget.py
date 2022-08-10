# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import subprocess, os, shutil
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
        self.hostFileSystemModel.setRootPath(os.path.expanduser('~'))
        self.guestFileSystemModel = QFileSystemModel()
        self.guestFileSystemModel.setRootPath(os.path.expanduser('~'))
        self.guestPath=""
        self.init_ui()
        self.guestCopyCandidate=""  # pathname for copying files within guestsystem, will be copied if user selects 'paste'

    def __del__(self):
        self.unmountDiskImage()

    def closeEvent(self, event):
        self.unmountDiskImage()


    def init_ui(self):
        self.ui = Ui_DiskImageWidget()
        self.ui.setupUi(self)
        self.ui.hostTreeView.setModel(self.hostFileSystemModel)
        self.ui.hostTreeView.setRootIndex(self.hostFileSystemModel.index(os.path.expanduser('~')));
        self.ui.guestTreeView.setModel(self.guestFileSystemModel)
        self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(os.path.expanduser('~')));
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
        menu = QMenu(self.ui.guestTreeView)
        newFolderAction = QAction("New Folder")
        newFolderAction.triggered.connect(self.createNewFolder)
        menu.addAction(newFolderAction)
        newFileAction = QAction("New Text File")
        newFileAction.triggered.connect(self.createNewFile)
        menu.addAction(newFileAction)
        menu.addSeparator()
        editAction = QAction("Edit")
        editAction.triggered.connect(self.editSelection)
        menu.addAction(editAction)
        renameAction = QAction("Rename")
        renameAction.triggered.connect(self.renameSelection)
        menu.addAction(renameAction)
        deleteAction = QAction("Delete")
        deleteAction.triggered.connect(self.deleteSelection)
        menu.addAction(deleteAction)
        menu.addSeparator()
        copyAction = QAction("Copy")
        copyAction.triggered.connect(self.copySelection)
        menu.addAction(copyAction)
        pasteAction = QAction("Paste")
        pasteAction.triggered.connect(self.pasteToSelection)
        menu.addAction(pasteAction)
        if self.guestCopyCandidate == "":
            pasteAction.setEnabled(False)
        else:
            pasteAction.setEnabled(True)
        menu.exec_(self.ui.guestTreeView.mapToGlobal(position))

    def copyToGuest(self):
        '''copies file highlighted in host view to guest'''
        # GUI uses single selection mode so can use the 0 index
        s = self.ui.hostTreeView.selectedIndexes()[0]
        d = self.ui.guestTreeView.selectedIndexes()[0]
        src = self.hostFileSystemModel.filePath(s)
        dest = self.guestFileSystemModel.filePath(d)
        print(f"Host to Guest: Copying {src} to {dest}")
        self.copyFile(src, dest)

    def copyToHost(self):
        '''copies file highlighted in guest view to host'''
        # GUI uses single selection mode so can use the 0 index
        s = self.ui.guestTreeView.selectedIndexes()[0]
        d = self.ui.hostTreeView.selectedIndexes()[0]
        src = self.guestFileSystemModel.filePath(s)
        dest = self.hostFileSystemModel.filePath(d)
        print(f"Guest to Host: Copying {src} to {dest}")
        self.copyFile(src, dest)

    def createNewFolder(self):
        '''Creates a new directory in the selected directory '''

    def createNewFile(self):
        '''Creates a new text file in the selected directory '''

    def editSelection(self):
        '''Edits selected file '''
        print("editing selection")


    def renameSelection(self):
        '''Renames selected file/folder '''
        print("editing selection")

    def deleteSelection(self):
        '''Deletes Edits selected file/folder '''
        print("Deleting selection")

    def copySelection(self):
        '''Copies Edits selected file/folder '''
        s = self.ui.guestTreeView.selectedIndexes()[0]
        self.guestCopyCandidate = self.guestFileSystemModel.filePath(s)
        print(f"Copying {self.guestCopyCandidate} to clipboard")

    def pasteToSelection(self):
        '''Pastes file/folder in selected folder'''
        print("Pasting selection")
        d = self.ui.guestTreeView.selectedIndexes()[0]
        dest = self.guestFileSystemModel.filePath(d)
        self.copyFile(self.guestCopyCandidate, dest)
        self.guestCopyCandidate = ""

    def copyFile(self, src, dest):
        '''copies a file at src to dest'''
        shutil.copy2(src, dest)

    def unmountDiskImage(self):
        ''' Unmount the guest FS'''
        if self.guestPath != "":
            mountOut = subprocess.run(["guestunmount", self.guestPath], capture_output=True)
            outStr = mountOut.stdout.decode("utf-8")
            print(f"Unmount output: {outStr}")
