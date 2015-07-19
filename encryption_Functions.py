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

# This have to be REVERSIBLE!! >_<
# 1. Count the string length
# 2. Convert it into a 4-digit number
#   - textfile needs to have no more than 9999 char per line
#	- Map the numbers of the 4-digits into another set of character
#	- Easy way of doing this is to take the [SHIFT] equivalent (eg. 1=!,2=@,3=#, etc.)
#	- IF a line has 9675 chars, THEN our 4-digit code will be "(^&%"
# 3. Our encrypted string would start with this 4-digit code
#   - eg. XXXX-------ENCRYPTED STRING-------... (where XXXX == 4-digit code)
# 3. 
# XXXX = 4 digit number to indicate how many char the string originally has
# 
1234 1234 1234 1234 1234 1234 1234 1234 1234 
	 VIDW PIDX VIDY PIDZ VIDW PIDX VIDY PIDZ // "WXYZ" is the 4-digit KEY that we have...

# This have to be REVERSIBLE!! >_<
# This have to be REVERSIBLE!! >_<
# This have to be REVERSIBLE!! >_<
#
# 1. Input strings are being divided into 2 classes,
# 	a. Length <= 100 chars
# 	b. Length > 100 chars
#
# a. We gotta extend these strings to meet the 100 char requirement
#    So we append a 4 digit code at the start to identify how to encrypt it...
#      - ">>XX" + "------encrypted_string-------...."
#      - >> = indicates that it's a class 1 string
#      - XX = indicates the original string length converted to it's [SHIFT] equivalent (eg. 1=!,2=@,3=#, etc.)
#      - eg. a string length of 65 will get aa 4 digit code ">>^%" (note that 65 was converted to its shift equivalent)
#
# b. No extension required
#    So we append a 4 digit code at the start to identify how to encrypt it...
#      - "????" + "------encrypted_string-------...."
#      - ???? = indicates that it's a class 2 string
#
# 2. Need to think of how to encypt the string lol...
#

def encryptThisString( inputString, VID, PID, Key ):

	strLength = len(inputString)
	if len <= 100:
		encryptedString = ">>"		# A class 1 string!
	else
		encryptedString = "????"	# A class 2 string!!

	# Insert main encyption algorithm here...

	return encryptedString

def decryptThisString( string, VID, PID, Key ):

	decryptedString = ""

	return decryptedString

#**********************************************************************
# TESTBENCH
#**********************************************************************
if __name__ == '__main__':

	sampleString = ""
	print( sampleString )
	print( encryptThisString(sampleString,"0000","FFFF",123456) )
	print( decryptThisString(sampleString,"0000","FFFF",123456) )

	input("Done")