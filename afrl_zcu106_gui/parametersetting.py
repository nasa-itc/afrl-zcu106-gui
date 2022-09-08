# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.

class parameterSetting:
    def __init__(self, name="", type="", notes=""):
        self.__name = name
        self.__type = type
        self.__notes = notes

    def __eq__(self, other):
        return (self.name() == other.name() and
                self.type() == other.type() and
                self.notes() == other.notes())

    def __lt__(self, other):
        if self.type() == other.type():
            return (self.name() < other.name())
        else:
            selfType = self.type()
            otherType = other.type()
            if 'int' in selfType:  #  group integer types together
                selfType='int'
            if 'int' in otherType:
                otherType = 'int'
            return (self.type().lower() < other.type().lower())

    def name(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def type(self):
        return self.__type

    def setType(self, type):
        self.__type = type

    def notes(self):
        return self.__notes

    def setNotes(self, notes):
        self.__notes = notes
