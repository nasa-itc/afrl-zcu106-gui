# Copyright (C) 2009 - 2022 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# This Python file uses the following encoding: utf-8

import subprocess, re
from afrl_gui.settingswidget import settingsWidget


class deviceSettingsWidget(settingsWidget):
    def __init__(self, parent, deviceStr):
        super().__init__(parent)
        self.paramStr = "-device"
        self.deviceStr = deviceStr
        self.headerPattern = re.compile(r".+ options:")
        self.infoDelimiter = ' - '
        self.typeStrip = '<>'
        self.populateForm()
