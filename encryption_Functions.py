#!/usr/bin/python

#----------------------------------------------------------------------
# Main Objective:
# Implement an algorithm to encrypt a textfile using a key & a USB device's VID, PID
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Approach :
# 1. Create a function that receives a string, VID, PID & Key 
#    -> apply the encryption algorithm on the string (using the other param)
#	 -> return the encrypted string
# 2. Encryption Algorithm:
# 	 -> Add a "checksum" at the start of the textfile to check whether
# 		the VID & PID of the current device matches the one used for encryption
#	 -> Will most likely add up the ASCII values of the (VID & PID) with the
#		string characters.
#	 -> The Key will be used to scramble the string even more xD
# 
# Of course, this would restrict the program to work with only ASCII-based
# textfiles...
#----------------------------------------------------------------------

def encryptThisString( string, VID, PID, Key ):

	encryptedString = ""

	return encryptedString