#!/usr/bin/env python3

"""
Notes: 
* Needs (un)zipped folder with master (blank) software files
* Needs a device list exported from PaperCut (private)
* Needs a list of devices that have a password and what those are (private)
* Probably set up for drag and drop to start
* Skip Smart SDK devices

- ask for software file or folder
- check that needed files exist
- get hostname
- check to see if that hostname is listed to have a password
    - get that password if so
- replace fields in properties file
    - hostname
    - server ip address
    - port
    - user
    - password
- save that file
- create zipped file with the hostname as the filename 
- sort into folder sorted by school


"""


import csv
import shutil
from pathlib import Path


# Get relative paths for files and folders needed (README.md)
# Unzipped folder containing PaperCut software files
PAPERCUT = Path(__file__).resolve().parent / 'private' / 'papercut_software'
# Device list from papercut
DEVICES = Path(__file__).resolve().parent / 'private' / 'device_list.csv'
# Admin-Generated device passwords list
PASSWORDS = Path(__file__).resolve().parent / 'private' / 'device_passwords.csv'



