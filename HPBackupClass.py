"""
This class is being created as a way to modularize the code to build many 
differing programs on the network.
"""
__author__ = 'Xander Petty'
__contact__ = 'Xander.Petty@protonmail.com'
__version__ = '1.0'

from netmiko import ConnectHandler
import os
import sys
import time

class ProCurveControl():
    def __init__(self, username, password, ip):
        self.netdatabase = {
            'device': {
                'username': username,
                'password': password,
                'ip': ip,
                'device_type': 'hp_procurve'
            },
            'connected': False,
            'root_location': str(os.getcwd()),
            'datetime': time.strftime("%m" + '-' + "%d" + '-' + "%Y") 
        }
    
    def connect_device(self):
        try:
            if self.netdatabase['connected'] == False:
                self.ssh = ConnectHandler(**self.netdatabase['device'])
                self.netdatabase.update({'connected': True}) 
                self.netdatabase.update({'device_name': str(self.ssh.base_prompt)})
            else:
                return str('You are already connected. Try disconnecting and try again.')
        except:
            return str('Could not connect to ' + str(self.netdatabase['device']['ip']))

    def disconnect_device(self):
        try:
            if self.netdatabase['connected'] == True:
                self.ssh.disconnect() 
                self.netdatabase.update({'connected': False})
            else:
                return str('You are already disconnected') 
        except:
            return str('Could not disconnect device')

    def save_config(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.ssh.save_config() 
                device_name = self.ssh.base_prompt
                sys.stdout = sys.__stdout__
                return str('Config saved on ' + str(device_name))
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not save config for ' + str(self.netdatabase['device']['ip']))
    
    def pull_startupconfig(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Pleae connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_startupconfig': self.ssh.send_command('show config')})
                sys.stdout = sys.__stdout__ 
                return str('Startup config saved to database')
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not pull startup config')
    
    def pull_runningconfig(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first') 
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_runningconfig': self.ssh.send_command('show run')})
                sys.stdout = sys.__stdout__ 
                return str('Running config saved to database')
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not pull running config') 

    def pull_logging(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w') 
                self.netdatabase.update({'raw_logging': self.ssh.send_command('show log -r')})
                sys.stdout = sys.__stdout__ 
                return str('Logging information saved to database')
        except:
            sys.stdout = sys.__stdout__
            return str('Could not pull logging information') 

    def pull_vlans(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_vlans': self.ssh.send_command('show vlan')})
                sys.stdout = sys.__stdout__ 
                return str('VLAN information saved to database')
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not pull vlan information') 

    def pull_dhcpsnooping(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_dhcpsnooping': self.ssh.send_command('show dhcp-snooping binding')})
                sys.stdout = sys.__stdout__ 
                return str('DHCP Snooping saved to database') 
        except:
            sys.stdout = sys.__stdout__
            return str('Could not pull dhcp snooping information') 
    
    def show_DBstartupconfig(self):
        try:
            print(self.netdatabase['raw_startupconfig'])
        except:
            return str('Could not find database copy of the startup-config')
    
    def show_DBrunningconfig(self):
        try:
            print(self.netdatabase['raw_runningconfig'])
        except:
            return str('Could not find database copy of the running-config')

    def show_DBlogging(self):
        try:
            print(self.netdatabase['raw_logging'])
        except:
            return str('Could not find database copy of logging info') 

    def show_DBvlans(self):
        try:
            print(self.netdatabase['raw_vlans'])
        except:
            return str('Could not find database copy of vlans info')

    def show_DBdhcpsnooping(self):
        try:
            print(self.netdatabase['raw_dhcpsnooping'])
        except:
            return str('Could not find database copy of dhcp snooping info') 

    def download_startupconfig(self):
        try:
            today = str("startupconfigs_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today))
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_startupconfig_" + self.netdatabase['datetime'] + ".pcc.txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_startupconfig'].splitlines():
                file.write(line)
                file.write("\n")
            file.close()
            os.chdir(str(self.netdatabase['root_location']))
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__
            return str('Could not save database copy of the startup config')

    def download_runningconfig(self):
        try:
            today = str("runningconfigs_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today)) 
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_runningconfig_" + self.netdatabase['datetime'] + ".pcc.txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_runningconfig'].splitlines():
                file.write(line)
                file.write("\n")
            file.close() 
            os.chdir(str(self.netdatabase['root_location']))
            sys.stdout = sys.__stdout__
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not save database copy of the running config') 

    def download_logging(self):
        try:
            today = str("logging_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today) 
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today)) 
            os.chdir(location) 
            filename = str(self.netdatabase['device_name'] + "_logging" + self.netdatabase['datetime'] + ".txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_logging'].splitlines():
                file.write(line)
                file.write("\n")
            file.close()
            os.chdir(str(self.netdatabase['root_location'])) 
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not save database copy of logging') 

    def download_vlans(self):
        try:
            today = str("vlans_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today)) 
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_vlans" + self.netdatabase['datetime'] + ".txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_vlans'].splitlines():
                file.write(line)
                file.write("\n")
            file.close()
            os.chdir(str(self.netdatabase['root_location'])) 
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__
            return str('Could not save database copy of vlans') 

    def download_dhcpsnooping(self):
        try:
            today = str("dhcpsnooping_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today))
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_dhcpsnooping" + self.netdatabase['datetime'] + ".txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_dhcpsnooping'].splitlines():
                file.write(line)
                file.write("\n")
            file.close() 
            os.chdir(str(self.netdatabase['root_location']))
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__
            return str('Could not save database copy of dhcp snooping')

