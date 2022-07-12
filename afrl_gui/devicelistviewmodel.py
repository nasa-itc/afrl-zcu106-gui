# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, Slot
from afrl_gui.qemuinstance import qemuInstance
from afrl_gui.common import MAXIMUM_QEMU_INSTANCES


class deviceListViewModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.deviceList = []
        self.deviceSettingsList = []
        self.validCount = 0

    def rowCount(self, QModelIndex):
        count = len(self.deviceList)
        print(f"rowCount Called, count: {count}")
        return count

    def data(self, index, role):
        row = index.row()
        print(f"deviceListViewModel.data() being called with index row: {row} and role : {role}")
        if(role == Qt.DisplayRole):
            print(f"DisplayRole: data returning {self.deviceList[row]}")
            return self.deviceList[row]

        elif(role == Qt.ToolTipRole):
            ds = self.deviceSettingsList[row]
            print(f"ToolTipRole: data returning {ds}")
            return self.deviceSettingsList[row]

        else:
            print(f"Role: {role}")

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, rows, index=QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)
        # data is inserted by insertQemuInstance slot
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def validDataCount(self):
        '''Returns the number of valid (non-empty) QEMU instances in fixed size list'''
        return self.validCount

    @Slot(str, list)
    def insertDevice(self, device, deviceSettings):
        row = len(self.deviceList)
        self.insertRows(row, 1)
        self.deviceList.append(device)
        self.deviceSettingsList.append(deviceSettings)
        topLeft = self.createIndex(row, 0)
        bottomRight = self.createIndex(row, 0)
        self.dataChanged.emit(topLeft, bottomRight)


