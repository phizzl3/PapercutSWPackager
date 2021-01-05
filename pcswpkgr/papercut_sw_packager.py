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
# User's Home / Downloads folder for output
DOWNLOADS = Path.home() / 'Downloads'




class Bundle():

    def __init__(self):
        pass


    def get_hostname(self):
        pass 


    def check_password(self):
        pass


    def create_package(self):
        pass


    def zip_files(self):
        pass


    

def generate_batch():
    """
    This needs to create a backup of the clean config file first
    and use a try/except to restore it just in case something fails
    """

    # Backup/Read clean config file
    with open(f'{PAPERCUT / "config.properties"}', 'r') as config_file:
        config_bak = config_file.read()


    try:
        
        machine_info = []

        with open(DEVICES, 'r') as device_list:
            # Skip extra header
            next(device_list)

            devices_csv = csv.DictReader(device_list)

            for line in devices_csv:
                if 'Smart' not in line['Device type']:
                    machine_info.append([
                        line['Device'].replace('device\\', ''),
                        line['Device groups'].replace('registration', '').strip('|')
                    ])






    except Exception as e:
        print(e)
        
        with open(f'{PAPERCUT / "config.properties"}', 'w') as config_file:
            config_file.write(config_bak)
        print(' Clean config.properties file restored.')




if __name__ == "__main__":
    generate_batch()
