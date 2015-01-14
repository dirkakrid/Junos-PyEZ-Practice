#!/usr/bin/python
from jnpr.junos import Device
from jnpr.junos.op.ethport import *
from jnpr.junos.op.phyport import *
#from jnpr.junos.op.vlan import *
from getpass import getpass
from pprint import pprint as pp
from os import system
import platform

#Prompt for username and password. This should be RADIUS info for the switch, router, firewall, etc.
username = raw_input("Username: ")
passwd = getpass()

def clearScreen():
	if platform.system() == "Windows":
		system('cls')
	elif platform.system() == "Linux":
		system('clear')
def listToDict(listName):
        index = 0
        newDict = {}
        for i in listName:
                newDict[index] = i
                index += 1
        return newDict
def listPorts(device):
	eths = EthPortTable(device).get()
	#Generate a dictionary from list returned from EthPortTable
	portDict = listToDict(eths.keys())
	#pp(eths.keys())
	pp(portDict)
	raw_input("Press [Enter] to continue...")
	clearScreen()
def individualPort(device):
    phyports = EthPortTable(device).get()
    clearScreen()
    ethPortDict = listToDict(phyports.keys())
    pp(ethPortDict)
    selection = int(raw_input("Select the index of the interface you would like to examine or press [Enter] to exit: "))
    while selection != "":
        port = ethPortDict[selection]
        if type(selection) is int and selection < len(phyports):
            print("Interface: " + port.key)
            if ( port.description is not None ):
                print(" Description:    "+ port.description)
            print(" Status:         " + port.admin + "/" + port.oper)
            print(" Flapped:        " + port.flapped)
            selection = raw_input("Select the index of the interface you would like to examine or press [Enter] to exit: ")
            clearScree()
        elif selection == "":
            break
        else:
            raw_input("Invalid entry. Please press [Enter] to continue.")
def deviceMenu():
	deviceOption = 1
	device = raw_input("Please enter device hostname or IP address: ")
	clearScreen()
	while deviceOption < 4:
		dev = Device(device,user=username,password=passwd)
		dev.open()
		print("DEVICE MENU\n\n")
		print("What would you like to do?")
		print(" 1) Get basic device statistics")
		print(" 2) Get basic information on all interfaces")
		print(" 3) Get basic information on a single interface")
		print(" 4) Exit this device")
		deviceOption = int(raw_input())
		if deviceOption == 1:
			#print("You chose 1")
			clearScreen()
			pp( dev.facts )
			raw_input("Press [Enter] to continue...")
		elif deviceOption == 2:
			#print("You chose 2")
			
			#Print some physical port statistics
			phyports = PhyPortTable(dev).get()
			eths = EthPortTable(dev).get()
			clearScreen()
			for port in phyports:
				print("Interface: " + port.key)
				if ( port.description is not None ):
					print(" Description:    "+ port.description)
				print(" Status:         " + port.admin + "/" + port.oper)
				print(" Flapped:        " + port.flapped)
			raw_input("Press [Enter] to continue...")
		elif deviceOption == 3:
			print("You chose 3")
			clearScreen()
			"""
			port = raw_input("Which port would you like to view?: ")
			print("Interface: " + port.key)
			if ( port.description is not None ):
				print(" Description:    "+ port.description)
			print(" Status:         " + port.admin + "/" + port.oper)
			print(" Flapped:        " + port.flapped)
			raw_input("Press Enter to continue...")
			"""
			listToDict
			#listPorts(dev)
			individualPort(dev)
			#eths = EthPortTable(dev).get()
			#pp(eths.keys())
			#raw_input("Press Enter to continue...")
			#clearScreen()
		elif deviceOption == 4:
			dev.close()
			clearScreen()
		else:
			print("Please enter a number 1-4")
mainMenu = 0
while mainMenu < 4:
	clearScreen()
	print("MAIN MENU\n\n")
	print("What would you like to do?")
	print(" 1) Select a device")
	print(" 2) Change username")
	print(" 3) Change password")
	print(" 4) Exit program")
	mainMenu = int(raw_input())
	if mainMenu == 1:
		deviceMenu()
	elif mainMenu == 2:
		username = raw_input("Username: ")
	elif mainMenu == 3:
		passwd = getpass()
	elif mainMenu == 4:
		clearScreen()
	else:
		print("Please enter a number 1-4.")


#Still trying to figure out how to print VLAN tags on specific interfaces
#vlans = VlanTable(dev).get()
#vlans = VlanView(dev).get()
#pp( vlans.tag() )

#I may need to pull VLAN tags from the configuration with something like the following:
# >show configuration interfaces port.key | match members
