# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
#
# This software is provided "as is" without any warranty of any, kind either express, implied, or statutory, including, but not
# limited to, any warranty that the software will conform to, specifications any implied warranties of merchantability, fitness
# for a particular purpose, and freedom from infringement, and any warranty that the documentation will conform to the program, or
# any warranty that the software will be error free.
#
# In no event shall NASA be liable for any damages, including, but not limited to direct, indirect, special or consequential damages,
# arising out of, resulting from, or in any way connected with the software or its documentation.  Whether or not based upon warranty,
#
# contract, tort or otherwise, and whether or not loss was sustained from, or arose out of the results of, or use of, the software,
# documentation or services provided hereunder
#
# ITC Team
# NASA IV&V
# ivv-itc@lists.nasa.gov

import afrl_zcu106_gui
import setuptools

setuptools.setup(
    name="afrl_zcu106_gui",
    version=afrl_zcu106_gui.__version__,
    description="AFRL ZCU106 QEMU GUI",
    author="ITC",
    author_email="ivv-itc@lists.nasa.gov",
    url="https://github.com/nasa-itc/afrl-rwwn",
    packages=setuptools.find_packages(),
    package_data={
        "afrl_zcu106_gui": [
        ],
    },
    entry_points={
        "gui_scripts": [
            "afrl_zcu106_gui = afrl_zcu106_gui.app:run",
        ]
    },
    install_requires=[
        "docker",
        "wheel",
        "pyqt5",
        "pygdbmi == 0.9.0.3",
        "sip"
    ],
    python_requires=">=3.4",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: System :: Emulators"
    ]
)

