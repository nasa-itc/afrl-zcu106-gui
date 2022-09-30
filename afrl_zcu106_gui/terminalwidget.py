# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QProcess, QProcessEnvironment


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

    def startXterm(self, name="", cmd="./test.sh"):
        geo = self.size()
        print("Terminal Geo: "+str(geo))

# This block sets xterm env but that gets wiped when bash starts
#        env = QProcessEnvironment.systemEnvironment()
#        print(f"env before change:{env.toStringList()}")
#        env.remove("PS1")
#        env.insert("PS1",f"{name}$")
#        print(f"env after change:{env.toStringList()}")
#        self.termProcess.setProcessEnvironment(env)

        argList = ["-into", str(int(self.winId())),
                   "-xrm", "'xterm*allowWindowOps: true'",
                   "-fg", "green",
                   "-aw",
                   "+fullscreen",
                   "-hold",
                   "-maximized",]
        if cmd:
            argList.extend(["-e",cmd, ])

        print("xterm arglist: "+str(argList))
        self.termProcess.start("xterm", argList)
        print("Terminal Started, PID: " + str(self.termProcess.processId()))
        return self.termProcess.processId()

    def stopXterm(self):
        self.termProcess.kill()
