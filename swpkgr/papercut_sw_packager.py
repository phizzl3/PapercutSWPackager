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
