# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

import re
from afrl_gui.settingswidget import settingsWidget


class machineSettingsWidget(settingsWidget):
    def __init__(self, deviceStr, parent=None):
        super().__init__(parent)
        self.paramStr = "-machine"
        self.deviceStr = deviceStr
        self.headerPattern = re.compile(r"NULL")
        self.infoDelimiter = ' ('
        self.notesStrip = ')'
        self.populateForm()
