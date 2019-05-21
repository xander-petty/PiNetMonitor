#!/usr/bin/local/python3.7
"""
    This is a simple script to modularize the notification system for the PiNetDevOps Platform
"""
__author__ = 'Xander Petty'
__contact__ = 'Xander.Petty@protonmail.com'
__version__ = '1.0'
import HPBackupClass as HPBC
import time 
import sys 

def main(NOCUser, NOCPass):
    datetime = time.strftime("%m" + '-' + "%d" + '-' + "%Y")
    filename = "warning_logs_" + str(datetime)
    file = open(filename, 'r')
    message = {
        'username': NOCUser,
        'password': NOCPass,
        'server': 'mailfront.noc.edu',
        'to': NOCUser,
        'subject': 'Daily Warning Logs Update',
        'body': file.read()
    }
    HPBC.send_email(**message)


myargs = {
    'NOCUser': sys.argv[1],
    'NOCPass': sys.argv[2]
}

main(**myargs)

