# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtCore import QProcess


class terminalWidget(QWidget):
    def __init__(self, parent):
        '''Constructor for terminalWindow'''
        QWidget.__init__(self)
        # super().__init__(self)
        # self.termProcess = QProcess(self.parent())
        self.termProcess = QProcess()

    def __del__(self):
        print("terminalWidget Destructor")
        self.stopXterm()

    def startXterm(self, name="", cmd="./test.sh"):
        geo = self.size()
        cols = int(geo.width()/6) #Estimate xterm geometry from widget size, 6,14 determined by observation
        lines=int(geo.height()/14)
        print(f"starting terminal size {cols}x{lines}")
        argList = ["-into", str(int(self.winId())),
                   #"-xrm", "'xterm*allowWindowOps: true'",
                   "-aw",
                   "-hold",
                   "-geometry",
                   f"{cols}x{lines}"]
        if cmd:
            argList.extend(["-e",cmd, ])

        self.termProcess.start("xterm", argList)
        print("Terminal Started, PID: " + str(self.termProcess.processId()))
        return self.termProcess.processId()

    def stopXterm(self):
        self.termProcess.kill()
