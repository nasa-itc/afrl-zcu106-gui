# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Collection of class definitions to define options for QEMU instance parameters

from afrl_gui.qemuparameter import qemuParameter


class qemuCpuItem(qemuParameter):

    def __repr__(self):
        '''Returns string representation of the qemu cpu options'''
        arg = self.argument()
        desc = self.description()
        return(f"CPU Item: arg: {arg} desc: {desc}")
