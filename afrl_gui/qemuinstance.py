# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHostAddress


class qemuInstance(QObject):
    def __init__(self):
        self.name = ""
        self.ipAddress = QHostAddress()
        self.subnetMask = QHostAddress()
        self.kernel = ""
        self.application = ""
        self.machine = ""
        self.cpu = ""
        self.devices = []

    def __repr__(self):
        '''Returns string representation of the qemu instance class'''
        return(f"""\nName: {self.name}
                   \nMachine: {self.machine}
                   \nCPU: {self.cpu}
                   \nIP: {self.ipAddress.toString()}
                   \nKernel: {self.kernel}
                   \nApplication: {self.application}""")

    def fieldCount(self):
        '''Returns the number of displayable fields for table views, update as necessary'''
        return 4
