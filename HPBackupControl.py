"""
This is a control script that is built on the BackupClass python module
It is intended to demonstrate the current features of the Python class
"""
__author__ = 'Xander Petty'
__contact__ = 'Xander.Petty@protonmail.com'
__version__ = '1.0' 

from sys import argv 
from HPBackupClass import ProCurveControl 
from multiprocessing.dummy import Pool 

def commands(username, password, ip):
    try:
        hp = ProCurveControl(username, password, ip)
        hp.connect_device()
        hp.save_config()
        hp.pull_startupconfig()
        hp.pull_runningconfig()
        hp.pull_logging()
        hp.pull_vlans()
        hp.pull_dhcpsnooping()
        hp.disconnect_device()
        hp.download_startupconfig()
        hp.download_runningconfig()
        hp.download_logging()
        hp.download_vlans()
        hp.download_dhcpsnooping()
        hp.show_DBrunningconfig()
        hp.show_DBstartupconfig()
        hp.show_BDlogging() 
        hp.show_DBvlans()
        hp.show_DBdhcpsnooping()
    except:
        print('Could not complete commands') 

def main(username, password):
    ips = []
    for ip in range(1, 27):
        ips.append('10.1.0.' + str(ip))
    pool = Pool(int(len(ips)))
    devices = []
    for ip in ips:
        temp = []
        temp.append(username)
        temp.append(password)
        temp.append(ip)
        devices.append(temp)
    dataout = pool.starmap(commands, devices)
    pool.close()
    pool.join()
    return dataout 


username = argv[1]
password = argv[2]
main(username, password)

