# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QProcess


class terminalWidget(QWidget):
    def __init__(self, parent):
        '''Constructor for terminalWindow'''
        QWidget.__init__(self)
        # super().__init__(self)
        # self.termProcess = QProcess(self.parent())
        self.termProcess = QProcess(self)

    def __del__(self):
        print("terminalWidget Destructor")
        self.stopXterm()

    def startXterm(self):
        geo = self.size()
        print("Terminal Geo: "+str(geo))
        argList = ["-into", str(int(self.winId())),
                   "-xrm", "'xterm*allowWindowOps: true'",
                   "-fg", "green",
                   "-fullscreen"]
        print("xterm arglist: "+str(argList))
        self.termProcess.start("xterm", argList)
        print("Terminal Started, PID: " + str(self.termProcess.processId()))
        return self.termProcess.processId()

    def stopXterm(self):
        self.termProcess.kill()
