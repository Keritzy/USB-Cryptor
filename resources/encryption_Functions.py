# #**********************************************************************
# # mainSequence
# #   - reads the OriginFile & writes the encrypted/decrypted results into the DestinationFile  
# #----------------------------------------------------------------------
# # PARAM:
# # keyCode - a string made up of the VID + PID + KEY
# # OriginFileName - Name of file to READ
# # DestinationFileName - Name of file to WRITE
# # mode - (1) = encryption & (2) = decryption
# #**********************************************************************
# def mainSequence( keyCode, OriginFileName, DestinationFileName, mode ):

# 	# Open the files for READING & WRITING
# 	OriginFile = open(OriginFileName,'r')
# 	DestinationFile = open(DestinationFileName,'w')
# 	error_flag = 0 

# 	# ENCRYPTION Sequence
# 	if mode==1:
# 		while True:
# 			tmpString = OriginFile.readline()
# 			if tmpString=="":
# 				break
# 			processedString = encryptThisString(tmpString,keyCode)
# 			DestinationFile.write(processedString)
# 	# DECRYPTION Sequence
# 	else:
# 		while True:
# 			# Identifies the class of the original string by extracting the first 6 bytes
# 			readString =  OriginFile.read(6)
			
# 			# Breaks loop when we're at EOF
# 			if readString=="":	
# 				break				

# 			originalStringLength = int( readString[2:6] )
# 			actualString = OriginFile.read(originalStringLength)
# 			processedString = decryptThisString(actualString,keyCode)
# 			DestinationFile.write(processedString)

# 	OriginFile.close()
# 	DestinationFile.close()

# 	return error_flag


#!/usr/bin/python
from tkinter import filedialog
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
	#		  --> 4 char format = ">>XXXX", where XXXX is the char length of the original string
	# Class 2 --> string that has >= 100 chars
	#		  --> 4 char format = "??XXXX", where XXXX is the char length of the original string
	encryptedString = ""
	if len(inputString) < 10:		encryptedString = ">>000" + str(len(inputString))
	elif len(inputString) < 100:	encryptedString = ">>00"  + str(len(inputString))
	elif len(inputString) < 1000:	encryptedString = "??0"   + str(len(inputString))
	else:							encryptedString = "??"    + str(len(inputString))    

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
		# print(inputString[i],end="")
		# print("+",end="")
		# print(keyCode[j],end="")
		# print("=",end="")
		# print(tmp_ASCII_value,end="")
		# print("=>",end="")

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		#print(tmp_ASCII_value)
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

	# # Identifies the class of the original string by extracting the first 6 chars
	# if ">>" in inputString:
	# 	originalStringLength = int( inputString[2:6] )
	# 	tmp_string = inputString[6:originalStringLength+6]
	# else:
	# 	tmp_string = inputString[6:(len(inputString)-1)]

	# Forces the input strings to be in ASCII-byte format instead of unicode
	# BYTE format required to carry out the decryption operation
	inputString = inputString.encode('ascii', 'ignore')
	keyCode = keyCode.encode('ascii', 'ignore')
	#****************************************************
	# Decryption Algorithm
	#****************************************************
	j = 0							
	for i in range( len(inputString) ):

		# Decrypts by reversing what was done in the encryption function
		tmp_ASCII_value = inputString[i] - keyCode[j]
		# print(inputString[i],end="")
		# print("-",end="")
		# print(keyCode[j],end="")
		# print("=",end="")
		# print(tmp_ASCII_value,end="")
		# print("=>",end="")

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		# print(tmp_ASCII_value)
		# Append the decrypted char to the rest of the decryptedString
		decryptedString = decryptedString + chr(tmp_ASCII_value)

		# Rotates the char used from keyCode on every iteration
		j = j + 1
		if j >= len(keyCode):	
			j = 0 

	# Returns the decrypted string	
	return decryptedString

def checkDecryptString(inputString):
	if inputString=="":
		return 0
	elif not( (inputString[0:2]==">>") or (inputString[0:2]=="??") ):
		return -1
	elif (inputString[2:6]).isdigit()==False:
		return -1
	else:
		return 1

#**********************************************************************
# mainSequence
#   - reads the OriginFile & writes the encrypted/decrypted results into the DestinationFile  
#----------------------------------------------------------------------
# PARAM:
# keyCode - a string made up of the VID + PID + KEY
# OriginFileName - Name of file to READ
# DestinationFileName - Name of file to WRITE
# mode - (1) = encryption & (2) = decryption
#**********************************************************************
def mainSequence( keyCode, OriginFileName, DestinationFileName, mode ):

	# Open the files for READING & WRITING
	OriginFile = open(OriginFileName,'r')
	DestinationFile = open(DestinationFileName,'w') 
	error_flag=0

	if mode==1:
		while True:
			tmpString = OriginFile.readline()
			# print("-------------------------------------------------------")

			# Breaks when read EOF
			if tmpString=="":		break

			# ENCRYPT string & write to output file
			processedString = encryptThisString(tmpString,keyCode)
			DestinationFile.write(processedString)
	else:
		while True:
			# Identifies the class of the original string by extracting the first 6 bytes
			readString =  OriginFile.read(6)
			#print(readString)

			# Checks if string is in "??XXXX" or ">>XXXX" format --> invalid ENCRYPTED file (if format mismatch)
			error_flag = checkDecryptString(readString)
			if error_flag==0:		break
			elif error_flag==-1:	break

			# Extract the actual string, excluding the "??XXXX" or ">>XXXX" at the front
			originalStringLength = int( readString[2:6] )
			actualString = OriginFile.read(originalStringLength)

			# IF specified & actual str_len doesn't match --> invalid ENCRYPTED file 
			if( len(actualString)!=originalStringLength ):
				error_flag = -1
				break

			# DECRYPT string & write to output file
			processedString = decryptThisString(actualString,keyCode)
			DestinationFile.write(processedString)

	# Close both read & write files when done
	OriginFile.close()
	DestinationFile.close()
	return error_flag

#**********************************************************************
# TESTBENCH
#**********************************************************************
if __name__ == '__main__':

	VID = "0000"
	PID = "1111"
	KeyNumber = "123456"
	keyCode = VID + PID + KeyNumber 

# 	# Testing encryptThisString() & decryptThisString() functions
# 	sampleString = "This is just a test"

# 	print( "Sample String:")
# 	print( sampleString )
# 	print( "")
# 	encryptedString = encryptThisString(sampleString,keyCode)
# 	print( "Encrypted String:")
# 	print( encryptedString )
# 	print( "")
# 	originalStringLength = int( encryptedString[2:6] )
# 	decryptedString = decryptThisString(encryptedString[6:originalStringLength+6],keyCode)
# 	print( "Decrypted String:")
# 	print( decryptedString )
# 	print( "")

	input("<<--End of Test-->>")
