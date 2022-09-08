# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Class to maintain list of QEMU machine (board) options

import subprocess
from afrl_gui.qemuparameterlist import qemuParameterList
from afrl_gui.qemumachineitem import qemuMachineItem


class qemuMachineList(qemuParameterList):
    def __init__(self):
        super().__init__()
        self.initializeList()

    def initializeList(self):
        qemuOut = subprocess.run(["./qemu-system-aarch64", "-machine", "?"], capture_output=True)
        if(qemuOut.returncode != 0):
            print(f"ERROR: qemu-system-aarch64 -machine ? returned error code: {qemuOut.returncode}")
            return
        outStr = qemuOut.stdout.decode("utf-8")
        values = outStr.split('\n')
        values = values[1:] # Trim off the header, TODO specify header for these returns to match and remove
        self.insertParameter(qemuMachineItem())  # Insert empty parameter as default value
        for v in values:
            if not v:
                continue # skip empty strings
            v = v.split(maxsplit=1)
            if(len(v) != 2):  # Each machine should be a arg, description pair so stop parsing on error or end of pairs
                break
            self.insertParameter(qemuMachineItem(arg=v[0], desc=v[1]))

    def __repr__(self):
        '''Returns string representation of the qemu machine option list '''
 #        return(f"{self.argument}: {self.description}")


