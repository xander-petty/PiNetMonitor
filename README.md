# PiNetMonitor
Python tool intended to run from a raspberry pi for HP network automation.

In order to prepare a Raspberry Pi, or any other Linux based system, Python3.7 is required. On the Raspberry Pi, you will have to compile it from source and then modify the ownerships and symbolic links to associate. 
Building a Python Virtual Environment is highly recommended when building and testing.

To achieve full automation, a control script must be created outlining the tasks to be performed and then a crontab is used to specify when to run the control program. 
