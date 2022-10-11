# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QHostAddress
from afrl_zcu106_gui.common import DOCKER_ROOT
from afrl_zcu106_gui.qemulauncher import run_qemu, stop_qemu
from datetime import datetime
import os, subprocess

class qemuInstance(QObject):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.interfaceName = ""
        self.ipAddress = QHostAddress()
        self.gateway = QHostAddress()
        self.subnetMask = QHostAddress()
        self.configFile = ""
        self.kernel = ""
        self.application = ""
        self.imageName = ""
        self.machine = ""
        self.machineSettings = []
        self.cpu = ""
        self.smpCores = ""
        self.cpuSettings = []
        self.memory = ""
        self.devices = []
        self.deviceSettings = []  # List of deviceSetting lists, index match devices[] list
        self.status = ""
        self.process = None


    def __repr__(self):
        '''Returns string representation of the qemu instance class'''
        return(f"""\nName: {self.name}
                   \nDescription: {self.description}
                   \nMachine: {self.machine}
                   \nCPU: {self.cpu}
                   \nSMP Cores: {self.smpCores}
                   \nMem: {self.memory}M
                   \nIP: {self.ipAddress.toString()}
                   \nImage: {self.imageName}
                   \nConfigFile: {self.configFile}
                   \nKernel: {self.kernel}
                   \nApplication: {self.application}
                   \nStatus: {self.status}""")

    def fieldCount(self):
        '''Returns the number of displayable fields for table views, update as necessary'''
        return 4

    def commandLine(self):
        '''Generates the qemu-system-aarch64 command line to launch this instance'''
        cmdLine = "qemu-system-aarch64"
        #Config file
        if self.configFile:
            cmdLine += f" -readconfig {self.configFile}"

        # Setup Machine
        if self.machine:
            cmdLine += f" -machine {self.machine}"
            for s in self.machineSettings:
                cmdLine += f",{s}"

        # Setup CPU
        if self.cpu != "":
            cmdLine += f" -cpu {self.cpu}"
            for s in self.cpuSettings:
                cmdLine += f",{s}"

        if self.smpCores == "ALL":
            cmdLine += " -smp $(nproc)"
        elif self.smpCores != "" and self.smpCores != "0":
            cmdLine += f" -smp {self.smpCores}"

        # Setup Memory
        if self.memory:
            cmdLine += f" -m {self.memory}M"  # Always using MB for simplicity

        # Setup devices
        deviceIdx = 0
        for d in self.devices:
            cmdLine += f" -device {d}"
            for s in self.deviceSettings[deviceIdx]:
                cmdLine += f",{s}"
            deviceIdx += 1

        # Setup drive
        # Currently constrained to single zcu106 SD image setup
        if self.imageName != "":
            cmdLine += f" -drive if=sd,format=raw,index=1,file={self.imageName}"
        return cmdLine

    def generateDockerEnvFile(self):
        '''Generate a env file containing env variables used to configure docker-compose instance'''
        if not self.name:
            return  #Only generate env files for named qemu configurations (.env is reserved for default config)

        fout = open(os.path.join(DOCKER_ROOT, f"{self.name}.env"),'w',encoding="utf-8")
        # Output Comment Block with Name, Description and date
        fout.write("#******************************************************************************\n")
        fout.write(f"#  {self.name}.env: docker-compose environment variable file for QEMU instance {self.name}\n")
        fout.write(f"#  Created: {datetime.now()}\n")
        fout.write(f"#  Description: {self.description}\n") # TODO: loop through description to only write x characters per line
        fout.write("#\n#******************************************************************************\n\n")
        fout.write("#The following is location of the config file for the ZCU106 QEMU instance\n")
        fout.write(f"QEMU_CONFIG_FILE={self.configFile}\n\n")
        fout.write("#The following is location of the root filesystem image file for the ZCU106 QEMU instance\n")
        fout.write(f"ROOT_IMAGE_FILE={self.imageName}\n\n")
        fout.write("#The following is the network adapter in the ZCU106 QEMU instance to configure (if applicable)\n")
        fout.write(f"NET_INTERFACE={self.interfaceName}\n\n")
        fout.write("#The following is IP Address for the ZCU106 QEMU instance\n")
        fout.write(f"IP_ADDRESS={self.ipAddress.toString()}\n\n")
        fout.write("#The following is the subnet mask for the ZCU106 QEMU instance\n")
        fout.write(f"SUBNET_MASK={self.subnetMask.toString()}\n\n")
        fout.write("#The following is the gateway for the ZCU106 QEMU instance\n")
        fout.write(f"GATEWAY={self.gateway.toString()}\n\n")
        fout.close()

    def generateCfgFile(self):
        ''' Generates an INI formatted config file for the -readconfig option '''
        subprocess.run(["mkdir", "-p", "./configs"])
        fout = open(f"{self.name}.cfg",'w',encoding="utf-8")
        

        # Setup Machine
        if self.machine != "":
            fout.write("[machine]\n")
            fout.write(f"    type={self.machine}\n")
            for s in self.machineSettings:
                fout.write(f"    {s}")

        # Setup CPU
        if self.cpu != "":
            fout.write(f"[cpu]\n    type={self.cpu}\n")
            for s in self.cpuSettings:
                fout.write(f"    {s}")
        if self.smpCores != "":
            fout.write("[smp-opts]\n")
            if self.smpCores == "ALL":
                fout.write("    cpus=$(nproc)\n")
            elif self.smpCores != "0":
                fout.write(f"    cpus={self.smpCores}\n")

        # Setup Memory
        if self.memory:
            fout.write(f"[memory]\n    size={self.memory}M\n")  # Always using MB for simplicity

        # Setup drive
        # Currently constrained to single zcu106 SD image setup
        if self.imageName != "":
            fout.write("[drive]\n")
            fout.write("    if=\"sd\"\n    format=\"raw\"\n    index=\"1\"\n")
            fout.write(f"file={self.imageName}")

        # Setup devices
        deviceIdx = 0
        for d in self.devices:
            fout.write(f"[device]\n    driver={d}\n")
            for s in self.deviceSettings[deviceIdx]:
                fout.write(f"    {s}\n")
            deviceIdx += 1
        fout.close()

    def startQemu(self):
        self.process = run_qemu(name = self.name, envFile = f"{self.name}.env")
        print(f"Process {self.process.pid} spawned for QEMU instance {self.name}")

    def stopQemu(self):
        stop_qemu(name = self.name)
        self.process.join()
