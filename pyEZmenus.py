#!/usr/bin/python
from jnpr.junos import Device
from jnpr.junos.op.ethport import *
from jnpr.junos.op.phyport import *
#from jnpr.junos.op.vlan import *
from getpass import getpass
from pprint import pprint as pp
from os import system
import platform
from jnpr.junos.utils.sw import SW

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
def individualPort(dev):
    phyports = PhyPortTable(dev).get()
    clearScreen()
    ethPortDict = listToDict(phyports.keys())
    for item in ethPortDict:
    	print(str(item) + ": " + ethPortDict[item])
    selection = raw_input("Select the index of the interface you would like to examine or press [Enter] to exit: ")
    while selection != "":
        selection = int(selection)
        port = selection
        if type(selection) is int and selection < len(phyports):
            print("Interface: " + phyports[port].key)
            if ( phyports[port].description is not None ):
                print(" Description:    "+ phyports[port].description)
            print(" Status:         " + phyports[port].admin + "/" + phyports[port].oper)
            print(" Flapped:        " + phyports[port].flapped)
            selection = raw_input("Select the index of the interface you would like to examine or press [Enter] to exit: ")
        elif type(selection) is None:
            break
        else:
            raw_input("Invalid entry. Please press [Enter] to continue.")
	clearScreen()
def viewInventory(dev):
	#Pull info on all transceivers, then print location, type, and name of transceiver
	from jnpr.junos.op.xcvr import XcvrTable
	xcvrDB = XcvrTable(dev).get()
	index = 0
	clearScreen()
	print dev.facts['model'] + " Chassis"
	print "	SN:	" + dev.facts['serialnumber']
	for item in xcvrDB:
		print "/".join(xcvrDB.keys()[index])
		print "	Type:	" + item.type
		print " SN:		" + item.sn
		index += 1
	raw_input("Press [Enter] to continue...")
	clearScreen()
def rebootDevice(dev):
	import time
	probe = False
	reboot = raw_input("Are you sure you would like to reboot? Enter Y to continue. :")
	if reboot == "Y" or reboot == "y":
		print("Rebooting device.")
		dev.sw.reboot(0)
		time.sleep(90)
		while probe != True:
			probe = dev.probe(15)
		print("Reboot complete.")
	else:
		clearScreen()
def upgradeJunos(dev):
	swPackage = raw_input("Please enter the filepath to the installer package: ")
	def myProgress(dev,msg):
		print "{}:{}".format(dev.hostname, msg)
	dev.sw.install(package=swPackage, progress=myProgress)
	print("Install has completed.")
	rebootDevice(dev)
	dev.open()
	print(dev.hostname + " has been upgraded to version " + dev.facts['version'])
def displayFacts(dev):
	for x in dev.facts:
		if type(dev.facts[x]) is dict:
			print str(x) + ':'
			for y in dev.facts[x]:
				if len(str(y)) < 6:
					print "			" + str(y) + ": " + "			" + str(dev.facts[x][y])
				elif len(str(y)) < 12:
					print "			" + str(y) + ": " + "		" + str(dev.facts[x][y])
				else:
					print "			" + str(y) + ": " + "	" + str(dev.facts[x][y])
			print ""
		elif str(dev.facts[x]) == "None":
			pass
		else:
			if len(str(x)) < 7:
				print str(x) + ": 			" + str(dev.facts[x])
			else:
				print str(x) + ":		" + str(dev.facts[x])
def deviceMenu():
	deviceOption = 1
	device = raw_input("Please enter device hostname or IP address: ")
	clearScreen()
	while deviceOption < 7:
		dev = Device(device,user=username,password=passwd)
		dev.bind(sw=SW)
		dev.open()
		print("DEVICE MENU\n\n")
		print("What would you like to do?")
		print(" 1) Get basic device statistics")
		print(" 2) Get basic information on all interfaces")
		print(" 3) Get basic information on a single interface")
		print(" 4) View device inventory")
		print(" 5) Upgrade this device")
		print(" 6) Reboot this device")
		print(" 7) Exit this device")
		deviceOption = int(raw_input())
		if deviceOption == 1:
			clearScreen()
			displayFacts(dev)
			raw_input("Press [Enter] to continue...")
		elif deviceOption == 2:
			#Print some physical port statistics
			phyports = PhyPortTable(dev).get()
			eths = EthPortTable(dev).get()
			clearScreen()
			for port in phyports:
				print(type(port))
				print("Interface: " + port.key)
				if ( port.description is not None ):
					print(" Description:    "+ port.description)
				print(" Status:         " + port.admin + "/" + port.oper)
				print(" Flapped:        " + port.flapped)
			raw_input("Press [Enter] to continue...")
		elif deviceOption == 3:
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
			viewInventory(dev)
		elif deviceOption == 5:
			upgradeJunos(dev)
		elif deviceOption == 6:
			rebootDevice(dev)
		elif deviceOption == 7:
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
