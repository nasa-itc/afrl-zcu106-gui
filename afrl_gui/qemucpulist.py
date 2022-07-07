# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Class to maintain list of QEMU CPU options

import subprocess
from afrl_gui.qemuparameterlist import qemuParameterList
from afrl_gui.qemucpuitem import qemuCpuItem


class qemuCpuList(qemuParameterList):
    def __init__(self):
        super().__init__()
        self.initializeList()

    def initializeList(self):
        qemuOut = subprocess.run(["./qemu-system-aarch64", "-cpu", "?"], capture_output=True)
        if(qemuOut.returncode != 0):
            print(f"ERROR: qemu-system-aarch64 -cpu ? returned error code: {qemuOut.returncode}")
            return
        outStr = qemuOut.stdout.decode("utf-8")
        values = outStr.split('\n')
        values = values[1:] # Trim off first line/header, TODO specify header for these returns to match and remove
        self.insertParameter(qemuCpuItem())  # Insert empty parameter as default value
        for v in values:
            if not v:
                continue # skip empty strings
            self.insertParameter(qemuCpuItem(arg=v.strip()))

    def __repr__(self):
        '''Returns string representation of the qemu cpu option list '''
 #        return(f"{self.argument}")


