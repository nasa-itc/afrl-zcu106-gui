# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHostAddress


class qemuInstance(QObject):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.ipAddress = QHostAddress()
        self.subnetMask = QHostAddress()
        self.kernel = ""
        self.application = ""
        self.machine = ""
        self.machineSettings = []
        self.cpu = ""
        self.cpuSettings = []
        self.memory = "4M"
        self.devices = []
        self.deviceSettings = []  # List of deviceSetting lists, index match devices[] list

    def __repr__(self):
        '''Returns string representation of the qemu instance class'''
        return(f"""\nName: {self.name}
                   \nDescription: {self.description}
                   \nMachine: {self.machine}
                   \nCPU: {self.cpu}
                   \nMem: {self.memory}M
                   \nIP: {self.ipAddress.toString()}
                   \nKernel: {self.kernel}
                   \nApplication: {self.application}""")

    def fieldCount(self):
        '''Returns the number of displayable fields for table views, update as necessary'''
        return 4

    def commandLine(self):
        '''Generates the qemu-system-aarch64 command line to launch this instance'''
        cmdLine = "qemu-system-aarch64"
        # Setup Machine
        if self.machine != "":
            cmdLine += f" -machine {self.machine}"
            for s in self.machineSettings:
                cmdLine += f",{s}"

        # Setup CPU
        if self.cpu != "":
            cmdLine += f" -cpu {self.cpu}"
            for s in self.cpuSettings:
                cmdLine += f",{s}"

        # Setup Memory
        cmdLine += f" -m {self.memory}M"  # Always using MB for simplicity

        # Setup devices
        deviceIdx = 0
        for d in self.devices:
            cmdLine += f" -device {d}"
            for s in self.deviceSettings[deviceIdx]:
                cmdLine += f",{s}"
            deviceIdx += 1

        return cmdLine


