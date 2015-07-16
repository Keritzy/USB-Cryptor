#!/usr/bin/python
#------------------------------------------------------
# Template
#------------------------------------------------------
# import win32com.client
# wmi = win32com.client.GetObject ("winmgmts:")
# for usb in wmi.InstancesOf ("Win32_USBHub"):
#      print(usb.DeviceID)
#------------------------------------------------------
#
# Main Objective: Obtain the device ID of any USB device being inserted
#
# Since we do not know the order of how the ID's are being retrieved, we 
# need to think of an algorithm to do it...
#
#------------------------------------------------------
# Approach #1: 
#------------------------------------------------------
# 1. Have for() loop to:
# 	- Make a super long string out of the device ID's
# 	- keep track of initial no. of devices
# 2. Try to decompose the long string into a list of device ID
# 3. After user has inserted a new USB device, implement an algorithm to 
#    compare & find the new device ID (using the list what we make in step 2)

import win32com.client

old_ID_string = []
new_ID_string = []
old_device_Count = 0
new_device_Count = 0
wmi = win32com.client.GetObject ("winmgmts:")

# Create a list of initial USB Device ID's
for usb in wmi.InstancesOf ("Win32_USBHub"):
      old_ID_string.append( str(usb.DeviceID) )		# Creates the list
      old_device_Count = old_device_Count + 1		# Keeps track of the # of ID's

# Prints the list out (for Debugging purposes)
for i in range(old_device_Count):
	print(old_ID_string[i])

#------------------------------------------------------------------
input("\nInsert USB device...\n")

# Create a new list of USB Device ID's
for usb in wmi.InstancesOf ("Win32_USBHub"):
      new_ID_string.append( str(usb.DeviceID) )		# Creates the list
      new_device_Count = new_device_Count + 1		# Keeps track of the # of ID's

# Prints the list out (for Debugging purposes)
for i in range(new_device_Count):
	print(new_ID_string[i])

# A series of checks to make sure there's only 1 new USB device ID
if not(new_device_Count > old_device_Count):
	print("Error: no new USB devices were detected...")

elif(new_device_Count != old_device_Count + 1):
	print("Error: More than 1 new USB devices were detected...")

else:

	device_ID = ""

	# Do a comparison betw. the lists to find the new USB device ID
	for i in range(new_device_Count):
		
		match_count = 0
		# checks if current string in the new list can be found in the old list
		for j in range(old_device_Count):
			# Tracks the # of matches
			if new_ID_string[i] in old_ID_string[j]:
				match_count = match_count + 1

		# If there wasn't any match, it means new_ID_string[i] is the new device ID!
		if match_count == 0:
			device_id = new_ID_string[i]
			print("New ID is:"+device_id)


