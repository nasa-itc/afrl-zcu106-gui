# Copyright (C) 2009 - 2020 National Aeronautics and Space Administration. All Foreign Rights are Reserved to the U.S. Government.
# 
# This software is provided "as is" without any warranty of any kind, either expressed, implied, or statutory, including, but not
# limited to, any warranty that the software will conform to specifications, any implied warranties of merchantability, fitness
# for a particular purpose, and freedom from infringement, and any warranty that the documentation will conform to the program, or
# any warranty that the software will be error free.
# 
# In no event shall NASA be liable for any damages, including, but not limited to direct, indirect, special or consequential damages,
# arising out of, resulting from, or in any way connected with the software or its documentation, whether or not based upon warranty,
# contract, tort or otherwise, and whether or not loss was sustained from, or arose out of the results of, or use of, the software,
# documentation or services provided hereunder.
# 
# ITC Team
# NASA IV&V
# ivv-itc@lists.nasa.gov

import os.path
from string import Template

#Path Variables
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCE_ROOT = os.path.join(PACKAGE_ROOT, "resources")
PROJECT_ROOT = os.path.normpath(os.path.join(PACKAGE_ROOT, "../../"))
DOCKER_ROOT = os.path.join(PROJECT_ROOT, "docker")
QEMU_ROOT = os.path.join(PROJECT_ROOT, "xilinx-qemu")
QEMU_BIN_DIR = os.path.join(QEMU_ROOT, "build/bin")


MAXIMUM_QEMU_INSTANCES = 8

#Filters for File Dialogs
QEMU_IMAGE_FILTERS = ["Disc Image files (*.img *.ext4)",
                      "All files (*)"]
QEMU_CFG_FILTERS = ["QEMU Config files (*.cfg)",
"All files (*)"]

# Text editor to call for editing files, include path if not on PATH
TEXT_EDITOR = "gedit"

#Guest Image Mount parameters
MOUNT_TIMEOUT = 90  #  Timeout to mout a guestimage in seconds

#networking configuration parameters for guest os
NETWORK_CFG = {
"CFG_FILE" : "/etc/network/interfaces",
"ADAPTER_NAME" : "eth0",
"IP_TEMPLATE" : Template("address $address"),
"NETMASK_TEMPLATE" : Template("netmask $netmask"),
"GATEWAY_TEMPLATE" : Template("gateway $gateway")
}

