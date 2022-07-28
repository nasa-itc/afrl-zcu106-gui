# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import subprocess, re, time, os
from PySide6.QtWidgets import QDockWidget, QFileSystemModel, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
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
        self.loopPaths = [] # stores paths of loop devices/objects that are mounted
        self.mountPaths = []
        self.partitionList = []
        self.init_ui()

    def __del__(self):
        self.unmountDiskImage()

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
        self.ui.guestComboBox.textActivated.connect(self.loadGuestImage)
        rhIcon = QIcon()
        rhIcon.addFile(os.path.join(RESOURCE_ROOT, "rhArrow.svg"), QSize(32,32),
                     QIcon.Normal, QIcon.On)
        self.ui.toGuestPushButton.setIcon(rhIcon)
        self.ui.toGuestPushButton.setIconSize(QSize(32,32))
        lhIcon = QIcon()
        lhIcon.addFile(os.path.join(RESOURCE_ROOT, "lhArrow.svg"), QSize(32,32),
                     QIcon.Normal, QIcon.On)
        self.ui.toHostPushButton.setIcon(lhIcon)
        self.ui.toHostPushButton.setIconSize(QSize(32,32))

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
        '''Creates a loop device for the image file at path and mounts as drive(s) '''
        diskOut = subprocess.run(["udisksctl", "loop-setup", "-f", path], capture_output=True)
        if(diskOut.returncode != 0):
            errorMsgBox(self, f"Cannot Mount Image at: {path}")
            return ""
        outStr = diskOut.stdout.decode("utf-8")
        # Parse outstr for the loop device to determine mount location
        m = re.match(r"Mapped file (?P<fileName>\S+) as (?P<loopName>\S+)\.", outStr)
        if m is None:
            errorMsgBox(self, f"Image {path} could not be opened\nError: {outStr}")
            return ""
        print(outStr)
        print(m.groupdict())
        loopPath = m.groupdict()['loopName']

        # Check to see if image loop is automounted
        time.sleep(3)  # Wait to allow time for automount
        self.getMountLocation(loopPath)
        if len(self.mountPaths) == 0:
            # If no  device mounted then attempt to mount the loop
            mountOut = subprocess.run(["udisksctl", "mount", "--block-device", loopPath], capture_output=True)
            outStr = mountOut.stdout.decode("utf-8")
            if(mountOut.returncode != 0):
                outErr = mountOut.stderr.decode("utf-8")
                errorMsgBox(self, f"Cannot Mount Loop Device {loopPath}\n{outErr}")
                return ""

        # add the mountPAths to the dropdown menu
        self.ui.guestComboBox.insertItems(0,self.mountPaths)
        print(f"Mounting complete, mounted drives: {self.mountPaths}")
        return self.mountPaths[0] # Return first mounted path on success

    def getMountLocation(self, devicePath):
        '''Get the mounted location of devicePath, returns empty string if not mounted '''
        if devicePath.startswith('/dev'):
            typeArg = '-b'
        elif devicePath.startswith('block_devices'):
            typeArg = '-p'
        else:
            print(f"{devicePath} is not a supported object nor block device")
            return

        loopOut = subprocess.run(['udisksctl', 'info', typeArg, devicePath], capture_output=True)
        if(loopOut.returncode != 0):
            outErr = loopOut.stderr.decode("utf-8")
            errorMsgBox(self, f"Cannot Access Device at: {devicePath}\n{outErr}")
            return ""

        outStr = loopOut.stdout.decode("utf-8")
        print(f"device info output: {outStr}")
        m = re.search(r"MountPoints:\s+(?P<mountPath>\S+)\s", outStr)
        if m is not None:
            mountPath = m.groupdict()['mountPath']
            print(f"Device {devicePath} mounted at: {mountPath}")
            self.mountPaths.append(mountPath)
            self.loopPaths.append(devicePath)
            return
        else:
            # Look for partitions
            m = re.search(r"Partitions:\s+\[(?P<partList>.+)\]\s", outStr)
            if m is not None:
                partitionStr = m.groupdict()['partList']
                self.partitionList = partitionStr.split(',')
                for i in range(0, len(self.partitionList)):
                    self.partitionList[i] = self.partitionList[i].strip()
                    self.partitionList[i] = self.partitionList[i].strip("'")
                    m = re.search(r"(?P<partPath>block_devices\S+)", self.partitionList[i])
                    if m is not None:
                        partPath = m.groupdict()['partPath']
                        print(f"Getting mount location for {partPath}")
                        self.getMountLocation(partPath) # recursive call to add the mount location for the partition
                    else:
                        print(f"re failed for {self.partitionList[i]}")

                print(f"Partitions: {self.partitionList}, Mount Points {self.mountPaths}")

    def unmountDiskImage(self):
        ''' Unmount and remove loop devices'''
        for f in self.loopPaths:
            if f.startswith('/dev'):
                typeArg = '-b'
            elif f.startswith('block_devices'):
                typeArg = '-p'
            else:
                print(f"{devicePath} is not a supported object nor block device")
                return
            mountOut = subprocess.run(["udisksctl", "unmount", typeArg, f], capture_output=True)
            outStr = mountOut.stdout.decode("utf-8")
            print(f"Unmount output: {outStr}")
