#!/usr/bin/python

#----------------------------------------------------------------------
# Main Objective:
# Obtain the Product ID (PID) & Vendor ID (VID) of any USB device being inserted
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Approach :
# 1. Make a function to create a list of USB device data (strings)
# 2. Obtain 2 list of USB device data (1x b4 plugging in the chosen USB device & 1x after)
# 3. Implement an algorithm to compare & find the new device ID (using the lists made in step 2)
# 4. Once ID is found, use another algorithm to extract the VID & PID (HEX)
#----------------------------------------------------------------------

import win32com.client

#**********************************************************************
# getDeviceIDList()
# - Retrieves a list containing info. of all connected USB devices
# - what we need is the VID & PID of the USB device
#----------------------------------------------------------------------
# RETURN:   
# device_list => list of USB device info
#**********************************************************************
def getDeviceIDList():

	wmi = win32com.client.GetObject ("winmgmts:")
	device_list = []
	device_count = 0

	# Create a list of initial USB Device ID's
	for usb in wmi.InstancesOf ("Win32_USBHub"):
		device_list.append( str(usb.DeviceID) ) # Creates the list

	# Prints the list out (for Debugging purposes)
	for i in range( len(device_list) ):
		print(device_list[i])

	return device_list

#**********************************************************************
# getNewDeviceID()
# - Compares the difference between the 2 input lists & returns it
#----------------------------------------------------------------------
# PARAM:
# oldList - list of USB data prior to insertion of the USB device
# newList - list of USB data after the insertion of the USB device
#----------------------------------------------------------------------
# RETURN:   
# -1 		=> if there's anything other than 1 new entry being detected
# device_ID => difference between the 2 input lists (i.e data string of the new USB device)
#**********************************************************************
def getNewDeviceID(oldList, newList):

	# Obtain the length of each list
	newListCount = len(newList)
	oldListCount = len(oldList)

	# Check to ensure there's only 1 new USB device ID
	if not( newListCount > oldListCount ):
		print("Error: no new USB devices were detected...")
	elif( newListCount != oldListCount+1 ):
		print("Error: More than 1 new USB devices were detected...")
	else:
		# Do a comparison betw. the lists to find the new USB device ID
		for i in range(newListCount):
			IDmatch = 0

			# checks if current string in the new list can be found in the old list
			for j in range(oldListCount):
				# Tracks the # of matches
				if newList[i] in oldList[j]:
					IDmatch = IDmatch + 1

			# If there wasn't any match, it means new_ID_string[i] is the new device ID!
			if IDmatch == 0:
				device_ID = newList[i]
				print("New ID is:"+device_ID)
				return device_ID
	
	return -1

#**********************************************************************
# extractID
#   - Compares the difference between the 2 input lists & returns it
#----------------------------------------------------------------------
# PARAM:
# id_string - string to extract values from
# tag - indicates the 4-digit HEX-value to extract (VID or PID) 
#----------------------------------------------------------------------
# RETURN:   
# tag_value => extracted value of the tag 
#			   (haven't decide what format I would want to play with)
#**********************************************************************
def extractID(id_string,tag):

	# eg. of ID = "USB\VID_XXXX&PID_YYYY\ZZZZZZ...."
	# .find gives us index of "V" of VID or "P" of PID
	index = id_string.find(tag)
	# +4 & +8 to get index of the 4th & 1st digit respectively
	tag_value = id_string[(index+4):(index+8)]
	print(tag_value)
	# Converts string representing base-16 integer -> decimal integer -> hex integer
	tag_value = hex(int(tag_value,16))

	return tag_value

#**********************************************************************
# TESTBENCH
#**********************************************************************
if __name__ == '__main__':

	# oldList = getDeviceIDList()
	# input("Insert the USB Device")
	# newList = getDeviceIDList()
	# USB_string = getNewDeviceID(oldList,newList)

	# if USB_string != -1:
	# 	input("extracting ID...")
	# 	extractID(USB_string,"PID")
	# 	extractID(USB_string,"VID")

	USB_string = "USB\VID_054C&PID_09C2\124861258912521"
	if USB_string != -1:
		input("extracting ID...")
		extractID(USB_string,"PID")
		extractID(USB_string,"VID")

	input("Done")

