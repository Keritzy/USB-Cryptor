#!/usr/bin/python

#----------------------------------------------------------------------
# Main Objective:
# Implement an algorithm to encrypt a textfile using a key & a USB device's VID, PID
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Approach :
# 1. Create a function that receives a string, KeyCode composed of VID, PID & KEY 
#    -> apply the encryption algorithm on the string (using the other param)
#	 -> return the encrypted string
# 2. Encryption Algorithm:
# 	 -> Add a "checksum" at the start of the textfile to check whether the VID & PID of the 
#		current device matches the one used for encryption (not sure if I want to implement this...)
#	 -> Will most likely add up the ASCII values of the KeyCode with the input string.
# 
# Of course, this would restrict the program to work with only ASCII-based textfiles... 
#----------------------------------------------------------------------

#**********************************************************************
# encryptThisString
#   - encrypts an input string using the key provided & returns it
#----------------------------------------------------------------------
# PARAM:
# inputString - Input string to be encrypted
# keyCode - a string made up of the VID + PID + KEY
#----------------------------------------------------------------------
# RETURN:   
# tag_value => encrypted string
#**********************************************************************
def encryptThisString( inputString, keyCode ):

	# Adds 4 chars @ the front of the string to identify the class of the original string
	# Class 1 --> string that has < 100 chars
	#		  --> 4 char format = ">>XX", where XX is the length of the original string
	# Class 2 --> string that has >= 100 chars
	#		  --> 4 char format = "????"
	encryptedString = ""
	if len(inputString) <= 10:		encryptedString = ">>0" + str(len(inputString))
	elif len(inputString) <= 100:	encryptedString = ">>" + str(len(inputString))
	else:							encryptedString = "????"

	# Append the string-to-be-encrypted w/ "!@#$%^&*()" until its length > 100
	while len(inputString) < 100:
		inputString = inputString + "!@#$%^&*()"

	# Forces the input strings to be in ASCII-byte format instead of unicode
	# BYTE format required to carry out the encryption operation
	inputString = inputString.encode('ascii', 'ignore')
	keyCode = keyCode.encode('ascii', 'ignore')

	#****************************************************
	# Encryption Algorithm
	#****************************************************
	j = 0
	# Encrypts the whole string char-by-char
	for i in range( len(inputString) ):
		
		# Encryption is done by adding ASCII values of the respective chars in both strings
		tmp_ASCII_value = inputString[i] + keyCode[j]

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		# Append the encrypted char to the rest of the encryptedString
		encryptedString = encryptedString + chr(tmp_ASCII_value)
		
		# Rotates the char used from keyCode on every iteration
		j = j + 1
		if j >= len(keyCode):	
			j = 0 

	# Returns the encrypted string
	return encryptedString

#**********************************************************************
# decryptThisString
#   - decrypts an input string using the key provided & returns it
#----------------------------------------------------------------------
# PARAM:
# inputString - Input string to be encrypted
# keyCode - a string made up of the VID + PID + KEY
#----------------------------------------------------------------------
# RETURN:   
# tag_value => decrypted string
#**********************************************************************
def decryptThisString( inputString, keyCode ):

	decryptedString = ""

	# Identifies the class of the original string by extracting the first 4 chars
	if ">>" in inputString:
		originalStringLength = int( inputString[2:4] )
		tmp_string = inputString[4:originalStringLength+4]
	else:
		tmp_string = inputString

	# Forces the input strings to be in ASCII-byte format instead of unicode
	# BYTE format required to carry out the decryption operation
	tmp_string = tmp_string.encode('ascii', 'ignore')
	keyCode = keyCode.encode('ascii', 'ignore')

	#****************************************************
	# Decryption Algorithm
	#****************************************************
	j = 0							
	for i in range( len(tmp_string) ):

		# Decrypts by reversing what was done in the encryption function
		tmp_ASCII_value = tmp_string[i] - keyCode[j]

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		# Append the decrypted char to the rest of the decryptedString
		decryptedString = decryptedString + chr(tmp_ASCII_value)

		# Rotates the char used from keyCode on every iteration
		j = j + 1
		if j >= len(keyCode):	
			j = 0 

	# Returns the decrypted string	
	return decryptedString

#**********************************************************************
# TESTBENCH
#**********************************************************************
if __name__ == '__main__':

	VID = "0000"
	PID = "1111"
	KeyNumber = "123456"
	sampleString = "This is just a test"
	keyCode = VID + PID + KeyNumber 

	print( "Sample String:")
	print( sampleString )
	print( "")
	encryptedString = encryptThisString(sampleString,keyCode)
	print( "Encrypted String:")
	print( encryptedString )
	print( "")
	decryptedString = decryptThisString(encryptedString,keyCode)
	print( "Decrypted String:")
	print( decryptedString )
	print( "")

	input("<<--End of Test-->>")

# #****************************************************
# # Used for debugging the decrypt & encrypt algorithm
# #****************************************************
# print(tmp_ASCII_value, end="")
# print("=", end="")
# print( inputString[i], end="")
# print("+", end="")
# print( keyCode[j], end="")
# print(" --> ", end="")