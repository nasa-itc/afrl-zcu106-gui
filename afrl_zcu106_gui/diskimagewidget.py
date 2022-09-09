    # This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import os, stat, shutil, subprocess
from PyQt5.QtWidgets import QAction, QWidget, QFileSystemModel, QFileDialog, QMenu, QInputDialog, QProgressDialog, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from afrl_zcu106_gui.ui.ui_diskimagewidget import Ui_DiskImageWidget
from afrl_zcu106_gui.errormsgbox import errorMsgBox
from afrl_zcu106_gui.common import QEMU_IMAGE_FILTERS, RESOURCE_ROOT, TEXT_EDITOR, MOUNT_TIMEOUT


class diskImageWidget(QWidget):

#    kill_signal = pyqtSignal(bool)

    def __init__(self, parent=None, path=""):
        super().__init__(parent)
        self.hostFileSystemModel = QFileSystemModel()
        self.hostFileSystemModel.setRootPath(os.path.expanduser('~'))
        self.guestFileSystemModel = QFileSystemModel()
        self.guestFileSystemModel.setRootPath(os.path.expanduser('~'))
        self.guestMountPoints={}
        self.init_ui()
        self.guestCopyCandidate=""  # pathname for copying files within guestsystem, will be copied if user selects 'paste'
        self.showDetails = False
        if path !="":
            self.openImageFile(path)

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
        self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(""));
        self.ui.guestTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.guestTreeView.customContextMenuRequested.connect(self.showFileContextMenu)
        self.ui.guestTreeView.setEnabled(False)
        self.showFileDetails(False)
        # Initialize comboboxes with Browse option, need to consider last few locations or default locations as well
        self.ui.hostComboBox.addItem("")
        self.ui.hostComboBox.addItem("Browse")
        self.ui.guestComboBox.addItem("")
        self.ui.guestComboBox.addItem("Select Image File...")
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
        self.ui.detailsPushButton.clicked.connect(self.toggleDetails)

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
        if path == "Select Image File...":
            fd = QFileDialog(self, "Open Guest Image")
            fd.setNameFilters(QEMU_IMAGE_FILTERS)
            if(fd.exec_()):
                filename = fd.selectedFiles()
                path = filename[0]
            if fd.close():  #Close the file dialog before loading image... first thing that doesn't work
                QApplication.processEvents() # force updates
                path = self.openImageFile(path)
                self.ui.guestComboBox.setCurrentIndex(0)  # Load the first entry

        if path.startswith("Image:"):
            self.guestFileSystemModel.setRootPath(self.guestMountPoints[path])
            self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(self.guestMountPoints[path]))
            self.ui.guestTreeView.setEnabled(True)

    def openImageFile(self, path):
        '''Opens image file with libguestfs and mounts the partition(s) '''
        guestPath = ""
        for idx in range(0,8):
            guestPath = f"{os.path.realpath(os.curdir)}/guestMnt{idx}"
            if os.path.isdir(guestPath) == False:
                subprocess.run(["mkdir", "-p", guestPath])
                break

        pd = QProgressDialog(f"Mounting {path}", "Cancel",0,MOUNT_TIMEOUT,self)
        pd.setMinimumDuration(0)  # Show the progress dialog as soon as mount starts
        pd.show()
        QApplication.processEvents() # force updates
        if pd.isVisible():
            diskOut = subprocess.Popen(["guestmount", "-a", path, "-o", f"uid={os.getuid()}", "-o", f"gid={os.getgid()}", "-i", guestPath])
            pd.canceled.connect(diskOut.terminate)
            timeout = MOUNT_TIMEOUT
            while timeout > 0:
                try:
                    diskOut.communicate(input=None, timeout=1)
                except subprocess.TimeoutExpired:
                    print(f"rc:{diskOut.returncode}")
                    pd.setValue(MOUNT_TIMEOUT - timeout)
                    QApplication.processEvents() # force updates
                if diskOut.returncode != None:
                    diskOut.terminate()
                    pd.close()
                    break
                timeout -= 1

            if(diskOut.returncode != 0):
                errorMsgBox(self, f"Cannot Mount Image at: {path}")
                diskOut.terminate()
                pd.close()
                return ""

            # add the mounted path to the dropdown menu
            imageStr = f"Image: {path}"
            self.ui.guestComboBox.insertItem(0,imageStr)
            print(f"Mounted {path} at {guestPath}")
            self.guestMountPoints[imageStr] = guestPath
            self.guestFileSystemModel.setRootPath(guestPath)
            self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(guestPath))
            self.ui.guestTreeView.setEnabled(True)
            return imageStr  #  Return the formatted image string on success

    def showFileContextMenu(self, position):
        '''displays context menu for file items in the treeviews '''
        selectedItem = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
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
        duplicateAction = QAction("Duplicate")
        duplicateAction.triggered.connect(self.duplicateSelection)
        menu.addAction(duplicateAction)
        copyAction = QAction("Copy")
        copyAction.triggered.connect(self.copySelection)
        menu.addAction(copyAction)
        pasteAction = QAction("Paste")
        pasteAction.triggered.connect(self.pasteToSelection)
        menu.addAction(pasteAction)
        #Set action enable
        if self.guestCopyCandidate == "":
            pasteAction.setEnabled(False)
        else:
            pasteAction.setEnabled(True)
        if os.path.isdir(selectedItem) == False:
            newFileAction.setEnabled(False)
            newFolderAction.setEnabled(False)
        else:
            editAction.setEnabled(False)

        menu.exec_(self.ui.guestTreeView.mapToGlobal(position))

    def showFilenameDialog(self,title="",origText=""):
        '''displays a dialog to get a name for new file, directory, duplicated file/dir, title argument allows customization to guide user '''
        [filename, ok] = QInputDialog.getText(self,title,"Name",text=origText)
        if ok:
            return filename
        else:
            return ""

    def copyToGuest(self):
        '''copies file highlighted in host view to guest'''
        # GUI uses single selection mode so can use the 0 index
        src = self.hostFileSystemModel.filePath(self.ui.hostTreeView.selectedIndexes()[0])
        dest = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        print(f"Host to Guest: Copying {src} to {dest}")
        self.copyTarget(src, dest)

    def copyToHost(self):
        '''copies file highlighted in guest view to host'''
        # GUI uses single selection mode so can use the 0 index
        src = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        dest = self.hostFileSystemModel.filePath(self.ui.hostTreeView.selectedIndexes()[0])
        print(f"Guest to Host: Copying {src} to {dest}")
        self.copyTarget(src, dest)

    def createNewFolder(self):
        '''Creates a new directory in the selected directory '''
        dest = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        name = self.showFilenameDialog("New Directory")
        if name:
            path = os.path.join(dest, name)
            if os.path.exists(path):
                errorMsgBox(self, f"Directory already exists at {path}")
                return
            os.mkdir(path)

    def createNewFile(self):
        '''Creates a new text file in the selected directory '''
        dest = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        name = self.showFilenameDialog("New Text File")
        if name:
            path = os.path.join(dest, name)
            if os.path.exists(path):
                errorMsgBox(self, f"File already exists at {path}")
                return
            open(path,'w')

    def editSelection(self):
        '''Edits selected file '''
        print("editing selection")
        path = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        if os.path.isdir(path):
            errorMsgBox(self, f"{path} is directory, cannot edit")
            return
        mode = os.stat(path).st_mode
        os.chmod(path,mode | stat.S_IWOTH)  # Set the Write permission for all to allow editor to save file
        os.system(f"{TEXT_EDITOR} {path}")
        os.chmod(path,mode) #  Restore original mode

    def renameSelection(self):
        '''Renames selected file/folder '''
        renamePath = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        [oldPath, oldName] = os.path.split(renamePath)
        description = "File"
        if os.path.isdir(renamePath):
            description = "Dir"
            #  TODO: Must handle directory differently, when it renames it breaks the file system model (renamed files in directory do not update on view)
        name = self.showFilenameDialog(f"Rename {description}", oldName)
        if name != "":
            path = os.path.join(oldPath, name)
            if os.path.exists(path):
                errorMsgBox(self, f"{description} already exists at {path}")
                return
            # TODO: Figure out how to get the model/view to update when directory is renamed
            #  if directory is renamed then a file in that directory is renamed it is not updated in view
            shutil.move(renamePath, path)

    def duplicateSelection(self):
        '''Duplicates selected file/folder, asks user for new name '''
        srcfile = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        srcPath = os.path.dirname(srcfile)
        [dest, filter]= QFileDialog.getSaveFileName(self, "Select Copy Destination",srcPath)
        if dest != "":
            self.copyTarget(srcfile,dest)

    def deleteSelection(self):
        '''Deletes Edits selected file/folder '''
        delFile = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        #  TODO add an are you sure?
        #Test if directory or file
        if os.path.isfile(delFile):
            os.remove(delFile)
        elif os.path.isdir(delFile):
            shutil.rmtree(delFile,False)

    def copySelection(self):
        '''Copies Edits selected file/folder '''
        self.guestCopyCandidate = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        print(f"Copying {self.guestCopyCandidate} to clipboard")

    def pasteToSelection(self):
        '''Pastes file/folder in selected folder'''
        dest = self.guestFileSystemModel.filePath(self.ui.guestTreeView.selectedIndexes()[0])
        print(f"Pasting selection: {self.guestCopyCandidate} to {dest}")
        self.copyTarget(self.guestCopyCandidate, dest)
        self.guestCopyCandidate = ""

    def copyTarget(self, src, dest):
        '''copies a file or directory at src to dest'''
        if os.path.isdir(dest):
            dest = dest + '/'  # Append a slash to make sure os treats as directory
        if os.path.isdir(src):
            dest = os.path.join(dest, os.path.basename(src))
            print(f"Copying directory {src} to {dest}")
            shutil.copytree(src,dest)
        else:
            shutil.copy2(src, dest)

    def unmountDiskImage(self):
        ''' Unmount the guest FS'''
        for name, mp in self.guestMountPoints.items():
            mountOut = subprocess.run(["guestunmount", mp], capture_output=True)
            outStr = mountOut.stdout.decode("utf-8")
            print(f"Unmounted {name}:{mp}, output: {outStr}")
            subprocess.run(["rm", "-rf", mp])  # Remove the directory after unmounting
            self.guestFileSystemModel.setRootPath("")
            self.ui.guestTreeView.setRootIndex(self.guestFileSystemModel.index(""));
            self.ui.guestTreeView.setEnabled(False)
            self.ui.guestComboBox.removeItem(self.ui.guestComboBox.findText(name))
        self.guestMountPoints.clear()

    def toggleDetails(self):
        if self.ui.detailsPushButton.text() == "Show Details":
            self.ui.detailsPushButton.setText("Hide Details")
            self.showFileDetails(True)
        else:
            self.ui.detailsPushButton.setText("Show Details")
            self.showFileDetails(False)


    def showFileDetails(self, visible=True):
        '''Displays all columns of file data in tree views'''
        for i in range(1,self.ui.guestTreeView.model().columnCount()):
            if visible:
                self.ui.guestTreeView.header().showSection(i)
                self.ui.hostTreeView.header().showSection(i)  # Same columns for both, toggle all at once
            else:
                self.ui.guestTreeView.header().hideSection(i)
                self.ui.hostTreeView.header().hideSection(i)  # Same columns for both, toggle all at once
