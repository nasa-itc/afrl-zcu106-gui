# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Collection of class definitions to define options for QEMU instance parameters

from afrl_gui.qemuparameter import qemuParameter


class qemuDeviceItem(qemuParameter):

    def __repr__(self):
        '''Returns string representation of the qemu machine options'''
        arg = self.argument()
        desc = self.description()
        alias = self.alias()
        bus = self.bus()
        return(f"Device Item: arg: {arg} desc: {desc} bus: {bus} alias: {alias}")

    def toolTipText(self):
        ttStr = ""
        if self.description() != "":
            ttStr = self.description()
        if self.bus() != "":
            ttStr = ttStr + f"\nBUS: {self.bus()}"
        if self.alias() != "":
            ttStr = ttStr + f"\nALIAS: {self.alias()}"
        return ttStr.strip()
