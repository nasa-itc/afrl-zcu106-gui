# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

# Baseclass for lists of candidates for QEMU parameters for dropdown comboboxes
from afrl_zcu106_gui.qemuparameter import qemuParameter

class qemuParameterList:
    def __init__(self):
        self.__paramList = []
        self.__argList = []
        self.__descList = []
        self.__busList = []

    def __getitem__(self, key):
        return self.__paramList[key]

    def __len__(self):
        return len(self.__paramList)

    def insertParameter(self, parameter):
        ''' Breaks parameter into components and stores in ordered lists '''
        self.__paramList.append(parameter)
        self.__argList.append(parameter.argument())
        self.__descList.append(parameter.description())
        self.__busList.append(parameter.bus())

    def argumentList(self):
        '''Returns a stringlist of the argument strings for QEMU'''
        return self.__argList

    def descriptionList(self):
        '''Returns a stringlist of the description strings when applicable (empty string if not) for QEMU argument'''
        return self.__descList

    def busList(self):
        '''Returns a stringlist of the bus strings when applicable (empty string if not) for QEMU argument'''
        return self.__busList
