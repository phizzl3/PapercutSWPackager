# papercut-sw-packager

Creates individual software bundles for installing PaperCut on RICOH MFD's and outputs .zip files to the user's Home / Downloads folder. Each .zip file will have a custom name and config.properties file that matches that specific machine's information and will be sorted into subfolders based on the machine's location.  

## Some of the required files are not included in this repo and are listed below.  

### These files will need to be present in the *private* folder  

* papercut_software **(Folder)** - Containing **All** of the installer, (clean) config, .jar files, etc,  
  just unzipped and dumped straight into this folder.  

* data.py - Containing the **hostname/ip address** and **Port** of the PaperCut server and the **username** for the machine.

```py
# example: 
SERVER = '10.10.10.10'  
PORT = '1234'
USER = 'administrator'
```

* device_list.csv - (Downloaded from PaperCut Admin > Devices > Export CSV) Containing the **device listing** along with the **location**, **hostname**, etc.  

* device_passwords.csv - (User/Admin Created) Containing the list of device **hostnames** and their associated **admin passwords**.  
