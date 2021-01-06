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
from private import data #NOTE: HAS VARS


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

    def __init__(self, name, group): #NOTE: ASSIGNS NAME/HOST AND GROUP
        self.name = name
        self.group = group



    # def get_hostname(self):
    #     pass 


    def get_password(self, passwords): #NOTE: GETS PASSWORD IF PRESENT, SETS NONE IF NOT
        self.password = passwords.get(self.name, None)


    def create_package(self, config):
        
        #NOTE REPLACE VALUES - WRITE OUT
        for field, info in (
            ('server-name=', data.SERVER),
            ('server-port=', data.PORT),
            ('admin-username=', data.USER),
            ('admin-password=', self.password),
            ('device-name=', self.name)
        ):
            if info: #NOTE: SKIP NONE VALUE (PWDS)
                config = config.replace(field, f'{field}{info}')

        

    def zip_files(self):
        pass


    

def generate_batch():
    """
    This needs to create a backup of the clean config file first
    and use a try/except to restore it just in case something fails
    """

    # Backup/Read clean config file
    with open(f'{PAPERCUT / "config.properties"}', 'r') as config_file: #NOTE: GETS CLEAN CONFIG FILE
        config_clean, config_bak = config_file.read(), config_file.read()


    try:
        

        with open(DEVICES, 'r') as device_list:
            # Skip extra header
            next(device_list)

            devices_csv = csv.DictReader(device_list) #NOTE: DICT OF LIST CSV

            #NOTE: MAKES LIST OF NAME, GROUP FROM CSV IF IT ISN'T A SMARTSDK DEV
            machine_info = [[line['Device'].replace('device\\', ''),
                line['Device groups'].replace('registration', '').strip('|')]
                for line in devices_csv if 'Smart' not in line['Device type']]

            
        #NOTE: PWDS FILE
        with open(PASSWORDS, 'r') as device_passwords:
            
            #NOTE: DICT OF CSV - EASIER TO WORK WITH
            passwords_csv = csv.DictReader(device_passwords)

            #NOTE: GEN DICT OF DEV: PWD FOR LATER
            password_info = {line['Device']: line['Password'] for line in passwords_csv}


        #NOTE: LOOP THROUGH MACHINES LIST
        for name, group in machine_info:

            #NOTE: CREATE OBJECT W/ ATTRS
            machine = Bundle(name, group)

            #NOTE: GET PW IF PRESENT
            machine.get_password(password_info)

            #NOTE: GEN PACKAGE
            machine.create_package(config_clean)
            

    #NOTE: EXEPTION IN CASE SOMETHING BREAKS
    except Exception as e:
        print(e)
        
        #NOTE: WRITE THE ORIGINAL CONFIG BACK IN CASE CHANGES WERE MADE
        with open(f'{PAPERCUT / "config.properties"}', 'w') as config_file:
            config_file.write(config_bak)
        print(' Clean config.properties file restored.')




if __name__ == "__main__":
    generate_batch()
