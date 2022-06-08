# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Base class for QEMU parameter items (e.g. machine, cpu, device)
class qemuParameter:
    def __init__(self, arg="", desc="", bus="", alias=""):
        self.__argument = arg
        self.__description = desc
        self.__bus = bus
        self.__alias = alias

    def __repr__(self):
        '''Returns string representation of the qemu machine options'''
        return(f"Argument: {self.__argument}\nDescription: {self.__description}\nBus: {self.__bus}")

    def setArgument(self, arg):
        ''' Sets the argument string '''
        self.__argument = arg

    def argument(self):
        ''' Returns argument string '''
        return self.__argument

    def setDescription(self, desc):
        ''' Sets the description string '''
        self.__description = desc

    def description(self):
        ''' Returns descripton string '''
        return self.__description

    def setBus(self, bus):
        ''' Sets the bus string '''
        self.__bus = bus

    def bus(self):
        ''' Returns bus string  '''
        return self.__bus

    def setAlias(self, alias):
        ''' Sets the alias string '''
        self.__alias = alias

    def alias(self):
        ''' Returns alias string  '''
        return self.__alias
