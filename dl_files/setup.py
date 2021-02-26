import glob
import os
from setuptools import setup, find_packages, Extension

def fileMake(path, source):
    isPath = False

    if os.path.isfile(path):
        with open(path) as lines:
            for line in lines:
               if line==source:
                   isPath = True

    if isPath==False:
        f = open(path, 'w')
        f.write(source)
        f.close()

    os.system('sudo chmod +x ' + path)

def make_sh():
    path = '/usr/bin/shutdown_wrc201.sh'
    cmd = '#!/bin/sh\ni2cset -y 1 0x10 0x0e 0x20 0x4e i \ni2cset -y 1 0x11 0x0e 0x20 0x4e i\ni2cset -y 1 0x12 0x0e 0x20 0x42 i\n'\
    'i2cset -y 1 0x13 0x0e 0x20 0x42 i\n\nexit 0'

    fileMake(path,cmd)

def make_service():
    path = '/etc/systemd/system/wrc201_off.service'
    service = '[Unit]\nDescription=vs-wrc201 shutdown\nBefore=shutdown.target\nDefaultDependencies=no\n'\
    '[Service]\nType=onehot\nExecStart=/usr/bin/shutdown_wrc201.sh\nRemainAfterExit=true\n'\
    '[Install]\nWantedBy=shutdown.target'

    fileMake(path,service)

    os.system('sudo systemctl enable wrc201_off.service')

os.system('sudo apt install i2c-tools')
make_sh()
make_service()

os.system('sudo pip install smbus')
