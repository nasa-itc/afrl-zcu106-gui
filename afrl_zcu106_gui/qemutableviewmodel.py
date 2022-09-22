# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSlot
from afrl_zcu106_gui.qemuinstance import qemuInstance
from afrl_zcu106_gui.common import MAXIMUM_QEMU_INSTANCES


class qemuTableViewModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.qemuList = []
        self.validCount = 0

    def __del__(self):
        for q in self.qemuList:
            q.stopQemu()

    def rowCount(self, QModelIndex):
        count = len(self.qemuList)
        # print(f"rowCount Called, count: {count}")
        return count

    def columnCount(self, QModelIndex):
        count = qemuInstance().fieldCount()
        # print(f"ColumnCount Called, count: {count}")
        return count

    def headerData(self, section, direction, role=Qt.DisplayRole):
        if direction == Qt.Horizontal and role == Qt.DisplayRole:
            headers = ["Name", "Application", "IP Address", "Status"]
            return headers[section]

    def data(self, index, role):
        #  print(f"data() being called with index: {index}, role: {role}")
        if(role == Qt.DisplayRole):
            col = index.column()
            if col == 0:
                return self.qemuList[index.row()].name
            elif col == 1:
                return self.qemuList[index.row()].application
            elif col == 2:
                return self.qemuList[index.row()].ipAddress.toString()
            elif col == 3:
                return self.qemuList[index.row()].status

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, rows, index=QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)
        # data is inserted by insertQemuInstance slot
        self.endInsertRows()
        return True

    def validDataCount(self):
        '''Returns the number of valid (non-empty) QEMU instances in fixed size list'''
        return self.validCount

    def insertQemuInstance(self, qemu):

        print("Table View Model Received QEMU instance: " + repr(qemu))
        print(f"cmd line: {qemu.commandLine()}")
        qemu.generateDockerEnvFile()
        # Following command launches the qemu instance, probably want to move it..
        qemu.startQemu()

        row = 0
        if len(self.qemuList) < MAXIMUM_QEMU_INSTANCES:
            row = len(self.qemuList)
            self.qemuList.append(qemu)
            self.insertRows(row, 1)
        else:
            for row in range(0, MAXIMUM_QEMU_INSTANCES):
                if not self.qemuList[row].name:
                    self.qemuList[row] = qemu
                    break
                if row == 7:
                    print("Maximum QEMU Instances reached")
        topLeft = self.createIndex(row, 0)
        bottomRight = self.createIndex(row, qemu.fieldCount())
        # Probably better add a better data validator prior to inserting to list
        if len(qemu.name):
            self.validCount = self.validCount + 1 # Don't forget to decrement when deleting
        self.dataChanged.emit(topLeft, bottomRight)
