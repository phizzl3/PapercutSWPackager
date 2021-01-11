#! /usr/bin/env python3
"""
Creates individual software bundles for installing PaperCut on RICOH MFD's 
and outputs .zip files to the user's Home / Downloads folder. Each .zip 
file will have a custom name and config.properties file that matches that 
specific machine's information and will be sorted into subfolders based 
on the machine's location. 
"""

import csv
import shutil
from pathlib import Path
from private import data
import copy
from tqdm import tqdm


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
    """
    Initialize objects and set name and group.
    """
    def __init__(self, name, group):
        self.name = name
        self.group = group




    def get_password(self, passwords):
        """
        Checks passwords dictionary for machine and sets associated 
        password if found. If no password is found, sets to None.

        Args:
            passwords (Dict): Contains machine names and associated admin passwords. 
                              {'machine': 'password'}

        Returns:
            self
        """
        self.password = passwords.get(self.name, None)

        return self


    def create_package(self, config):  #TODO RENAME THIS TO GENERATE CONFIG
        """
        Generates 'config.properties' file with the needed information 
        for the specific machine. 

        Args:
            config (Str): String containing the contents of the original 
                          'config.properties' file to be updated and written out.

        Returns:
            self
        """
        # Find and replace fields with new values for machine
        for field, info in (
            ('server-name=', data.SERVER),
            ('server-port=', data.PORT),
            ('admin-username=', data.USER),
            ('admin-password=', self.password),
            ('device-name=', self.name)
        ):
            # Replace fields, skipping None values (passwords)
            if info:
                config = config.replace(field, f'{field}{info}')

        # Write contents out to disk for use in packaging bundle
        with open(PAPERCUT / 'config.properties', 'w') as out_config:
            out_config.write(config)

        return self



    def zip_files(self):
        """
        Gets the contents of the 'papercut_software' folder (which should 
        include an updated 'properties.config') and zips the contents to 
        the user's Home / Downloads folder and sorts them into subfolders 
        based on the machine's location.

        Returns:
            self
        """
        shutil.make_archive(
            DOWNLOADS / 'PaperCut_Packages' / self.group.title() / self.name,
            'zip',
            PAPERCUT
        )

        return self

    

def generate_batch():
    """
    Main script - Reads the clean 'properties.config' file from the 'papercut_software' 
    folder and creates a working copy to use with the class methods so that a clean 
    copy can be used each loop or restored if something crashes and then calls the methods 
    to get all of the specific info, generate the config file, and then output the final, 
    sorted .zip file bundles.
    """
    # Read clean config file
    with open(f'{PAPERCUT / "config.properties"}', 'r') as config_file:
        clean_config = config_file.read()
        # Make a working copy of the config        
        working_config = copy.deepcopy(clean_config)


    try:        
        # Open the device list and set up a Dict reader
        with open(DEVICES, 'r') as device_list:
            # Skip extra header
            next(device_list)
            devices_csv = csv.DictReader(device_list)

            # Make a list of name and group from the CSV file, skipping SmartSDK Devices
            machine_info = [[line['Device'].replace('device\\', ''),
                line['Device groups'].replace('registration', '').strip('|')]
                for line in devices_csv if 'Smart' not in line['Device type']]

        # Open the passwords file and set up a Dict Reader            
        with open(PASSWORDS, 'r') as device_passwords:
            passwords_csv = csv.DictReader(device_passwords)

            # Generate a dictionary of the names and passowords to ease my life
            password_info = {line['Device']: line['Password'] for line in passwords_csv}


        #NOTE: LOOP THROUGH MACHINES LIST   NOTE: STATUS? 
        for name, group in tqdm(machine_info):

            #NOTE: CREATE OBJECT W/ ATTRS
            machine = Bundle(name, group)

            #NOTE: GET PW IF PRESENT
            machine.get_password(password_info)

            #NOTE: GEN PACKAGE
            machine.create_package(working_config)

            #NOTE: ZIP THE FILES
            machine.zip_files()

   

            #NOTE: REST CLEAN CONFIG
            with open(PAPERCUT / 'config.properties', 'w') as restore_config:
                restore_config.write(clean_config)
            

    #NOTE: EXEPTION IN CASE SOMETHING BREAKS
    except Exception as e:
        print(e)
        
        #NOTE: WRITE THE ORIGINAL CONFIG BACK IN CASE CHANGES WERE MADE
        with open(f'{PAPERCUT / "config.properties"}', 'w') as config_file:
            config_file.write(clean_config)
        print(' Clean config.properties file restored.')




if __name__ == "__main__":
    generate_batch()
