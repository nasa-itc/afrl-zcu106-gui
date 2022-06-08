# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Class to maintain list of QEMU machine (board) options

import re, subprocess
from afrl_gui.qemuparameterlist import qemuParameterList
from afrl_gui.qemudeviceitem import qemuDeviceItem


class qemuDeviceList():
    def __init__(self):
        super().__init__()
        self.__deviceTypeList = [] # List of each type of device
        self.__deviceLists = [] # A list of qemuParameterLists, each list corresponding to a type in __deviceTypeList
        self.initializeList()

    def deviceTypeList(self):
        return self.__deviceTypeList

    def deviceLists(self):
        return self.__deviceLists

    def initializeList(self):
        qemuOut = subprocess.run(["./qemu-system-aarch64", "-device", "?"], capture_output=True)
        if(qemuOut.returncode != 0):
            print(f"ERROR: qemu-system-aarch64 -device ? returned error code: {qemuOut.returncode}")
            return
        outStr = qemuOut.stdout.decode("utf-8")
        # Parse out the device types for filtering

        # Parse out all the device candidates
        values = outStr.split('\n')  # Split into lines, process each line
        headerPattern = re.compile(r".+ devices")
        for v in values:
            if not v:
                continue # skip empty strings
            #Check for a new device type
            header = headerPattern.match(v)
            if header is not None:
                type = re.split(r"\sdevices:",v,maxsplit=1)
                self.__deviceTypeList.append(type[0])
                print(self.__deviceTypeList)
                self.__deviceLists.append(qemuParameterList())
                continue  # Check Next line
            # Must be a device listing
            listIdx = len(self.__deviceLists) - 1
            params = v.split(',')
            device = qemuDeviceItem()
            for p in params:
                p = p.strip()
                if p.find("name") == 0:
                    device.setArgument(p.replace('name "','').strip('"').strip())
                if p.find("bus") == 0:
                    device.setBus(p.replace('bus ', '').strip())
                if p.find("desc") == 0:
                    device.setDescription(p.replace('desc "', '').strip('"').strip())
                if p.find("alias") == 0:
                    device.setAlias(p.replace('alias "', '').strip('"').strip())
            self.__deviceLists[listIdx].insertParameter(device)

    def __repr__(self):
        '''Returns string representation of the qemu device option list '''
 #        return(f"{self.argument}: {self.description}")


