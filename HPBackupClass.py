"""
This class is being created as a way to modularize the code to build many 
differing programs on the network.
"""
__author__ = 'Xander Petty'
__contact__ = 'Xander.Petty@protonmail.com'
__version__ = '1.2'

from netmiko import ConnectHandler
import os
import sys
import time
import smtplib
from email.mime.text import MIMEText 

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

    def pull_portsecurity(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_portsecurity': self.ssh.send_command('show port-security')})
                sys.stdout = sys.__stdout__ 
                return str('Port Security saved to database') 
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not pull Port Security information')

    def pull_interfacebrief(self):
        try:
            if self.netdatabase['connected'] == False:
                return str('Please connect device first')
            else:
                sys.stdout = open(os.devnull, 'w')
                self.netdatabase.update({'raw_interfacebrief': self.ssh.send_command('show interface brief')})
                sys.stdout = sys.__stdout__
                return str('interface brief added to database')
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not pull interface brief') 
    
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

    def show_DBportsecurity(self):
        try:
            print(self.netdatabase['raw_portsecurity'])
        except:
            return str('Could not find database copy of port security info') 

    def show_DBinterfacebrief(self):
        try:
            print(self.netdatabase['raw_interfacebrief'])
        except:
            return str('Could not find database copy of interface brief info') 

    def return_DBstartupconfig(self):
        try:
            return self.netdatabase['raw_startupconfig']
        except:
            return str('Could not find startup config in database')

    def return_DBrunningconfig(self):
        try:
            return self.netdatabase['raw_runningconfig']
        except:
            return str('Could not find running config in database')

    def return_DBlogging(self):
        try:
            return self.netdatabase['raw_logging']
        except:
            return str('Could not find logging info in database')

    def return_DBvlans(self):
        try:
            return self.netdatabase['raw_vlans']
        except:
            return str('Could not find vlans info in database')
    
    def return_DBdhcpsnooping(self):
        try:
            return self.netdatabase['raw_dhcpsnooping']
        except:
            return str('Could not find dhcp snooping in database')
        
    def return_DBportsecurity(self):
        try:
            return self.netdatabase['raw_portsecurity']
        except:
            return str('Could not find port security in database') 

    def return_DBinterfacebrief(self):
        try:
            return self.netdatabase['raw_interfacebrief']
        except:
            return str('Could not find interface brief in database') 

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

    def download_portsecurity(self):
        try:
            today = str("portsecurity_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today))
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_portsecurity" + self.netdatabase['datetime'] + ".txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_portsecurity'].splitlines():
                file.write(line)
                file.write("\n")
            file.close()
            os.chdir(str(self.netdatabase['root_location']))
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__
            return str('Could not save database copy of port security')

    def download_interfacebrief(self):
        try:
            today = str("interfacebrief_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            if not os.listdir(str(self.netdatabase['root_location'])).__contains__(today):
                os.mkdir(str(self.netdatabase['root_location'] + '/' + today))
            os.chdir(location)
            filename = str(self.netdatabase['device_name'] + "_interfacebrief" + self.netdatabase['datetime'] + ".txt")
            file = open(filename, 'a')
            sys.stdout = open(os.devnull, 'w')
            for line in self.netdatabase['raw_interfacebrief'].splitlines():
                file.write(line)
                file.write("\n")
            file.close()
            os.chdir(str(self.netdatabase['root_location'])) 
            sys.stdout = sys.__stdout__
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not save database copy of interface brief') 

    def append_alertlog(self):
        try:
            today = str("intrusion_alerts_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today) 
            os.chdir(location) 
            file = open(today, 'a')
            sys.stdout = open(os.devnull, 'w')
            sec = self.return_intrusionalerts()
            file.write(str(self.netdatabase['device_name']))
            file.write("\n")
            for line in sec:
                file.write(line)
                file.write("\n")
            file.close() 
            os.chdir(str(self.netdatabase['root_location'])) 
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could no append intrusion log') 

    def append_warninglog(self):
        try:
            today = str("warning_logs_" + self.netdatabase['datetime'])
            location = str(self.netdatabase['root_location'] + '/' + today)
            os.chdir(location)
            file = open(today, 'a')
            sys.stdout = open(os.devnull, 'w')
            loggs = self.return_warning_logs()
            file.write(str(self.netdatabase['device_name']))
            file.write("\n")
            for line in loggs:
                file.write(line)
                file.write("\n")
            file.close() 
            os.chdir(str(self.netdatabase['root_location'])) 
            sys.stdout = sys.__stdout__ 
        except:
            sys.stdout = sys.__stdout__ 
            return str('Could not append warning log') 

    def return_warning_logs(self):
        try:
            loggs = self.netdatabase['raw_logging'].splitlines()
            for line in range(0, 3):
                loggs.remove(loggs[0])
            warnings = []
            for line in loggs:
                if line[0] == 'W':
                    if not line.__contains__('snmp'):
                        warnings.append(line)
            return warnings 
        except:
            return str('Could not filter warning messages')

    def return_intrusionalerts(self):
        # NOTE: This one isn't working.
        try:
            sec = self.netdatabase['raw_portsecurity'].splitlines()
            for line in range(0, 6):
                sec.remove(sec[0])
            sec.remove(sec[len(sec) - 1])
            alerts = []
            for line in sec:
                if line[4] == ' ':
                    if line[20] == 'Y':
                        iface = str(line[2] + line[3])
                        alerts.append(iface)
                else:
                    if line[21] == 'Y':
                        iface = str(line[2] + line[3] + line[4])
                        alerts.append(iface) 
            return alerts 
        except:
            return str('Could not gather intrusion alerts') 


def send_email(username, password, server, to, subject, body):
    try:
        mailserver = smtplib.SMTP(server, '25')
        mailserver.login(username, password)
        message = MIMEText(body)
        message['To'] = to
        message['From'] = username
        message['Subject'] = subject
        text = message.as_string()
        mailserver.sendmail(to, username, text)
    except:
        return str('Could not send email to ' + str(to))


