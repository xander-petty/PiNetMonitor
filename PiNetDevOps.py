"""
    This is the control program for running automation on the Raspberry Pi.
    Higher level functions and commands will be build here and built on the lower level HPBackupClass
"""
__author__ = 'Xander Petty'
__contact__ = 'Xander.Petty@protonmail.com'
__version__ = '2.0'

from sys import argv 
import HPBackupClass as HBC 
from multiprocessing.dummy import Pool 
import os 
import time 

def commands(username, password, ip, rootlocation, datetime):
    try:
        device = {
            'username': username,
            'password': password,
            'ip': ip 
        }
        hp = HBC.ProCurveControl(**device)
        hp.connect_device()
        hp.save_config()
        create_database(hp)
        download_database(hp)
        create_log(hp, rootlocation, datetime)
        hp.disconnect_device()
    except:
        print('Could not complete command list') 

def create_database(device):
    try:
        device.pull_startupconfig()
        device.pull_runningconfig()
        device.pull_logging()
        device.pull_vlans()
        device.pull_dhcpsnooping()
        device.pull_portsecurity()
        device.pull_interfacebrief() 
    except:
        print('Could not complete pull commands to build the database')

def download_database(device):
    try:
        device.download_startupconfig()
        device.download_runningconfig()
        device.download_logging()
        device.download_vlans()
        device.download_dhcpsnooping()
        device.download_portsecurity()
        device.download_interfacebrief()
    except:
        print('Could not complete download of database') 

def create_log(device, rootlocation, datetime):
    warn = device.return_warning_logs()
    #logg = device.return_intrusionalerts() 
    warning_file = open(str("warning_logs_" + datetime), 'a')
    #alert_file = open(str("intrusion_alerts_" + datetime), 'a') 
    warning_file.write(str(device.netdatabase['device_name'])) 
    warning_file.write("\n")
    for line in warn:
        warning_file.write(line)
        warning_file.write("\n")
    warning_file.write("\n")
    warning_file.close()
    # warning_file = open(str("warning_logs_" + datetime), 'r').read() 

def main(username, password, NOCUser, NOCPass):
    rootlocation = str(os.getcwd()) 
    datetime = time.strftime("%m" + '-' + "%d" + '-' + "%Y") 
    ips = []
    for ip in range(0, 27):
        ips.append('10.1.0.' + str(ip))
    pool = Pool(int(len(ips)))
    devices = []
    for ip in ips:
        temp = []
        temp.append(username)
        temp.append(password)
        temp.append(ip)
        temp.append(rootlocation)
        temp.append(datetime)
        devices.append(temp) 
    dataout = pool.starmap(commands, devices)
    pool.close()
    pool.join()
    return dataout


connect = {
    'username': argv[1],
    'password': argv[2],
    'NOCUser': argv[3],
    'NOCPass': argv[4]
}
main(**connect)
