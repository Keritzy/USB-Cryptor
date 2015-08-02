#!/usr/bin/python
from tkinter import filedialog

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
		print(inputString[i],end="")
		print("+",end="")
		print(keyCode[j],end="")
		print("=",end="")
		print(tmp_ASCII_value,end="")
		print("=>",end="")

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		print(tmp_ASCII_value)
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
		print(inputString[i],end="")
		print("-",end="")
		print(keyCode[j],end="")
		print("=",end="")
		print(tmp_ASCII_value,end="")
		print("=>",end="")

		# If the values exceed the ASCII range of 0~127, make it overflow/underflow
		if tmp_ASCII_value < 0:
			tmp_ASCII_value = tmp_ASCII_value + 127
		elif tmp_ASCII_value > 127:
			tmp_ASCII_value = tmp_ASCII_value - 127

		print(tmp_ASCII_value)
		# Append the decrypted char to the rest of the decryptedString
		decryptedString = decryptedString + chr(tmp_ASCII_value)

		# Rotates the char used from keyCode on every iteration
		j = j + 1
		if j >= len(keyCode):	
			j = 0 

	# Returns the decrypted string	
	return decryptedString

#**********************************************************************
# checkDecryptString 
#   - check if inputString adheres to the format of an ENCRYPTED string
#----------------------------------------------------------------------
# PARAM:
# inputString - string to check
#----------------------------------------------------------------------
# RETURN:
#  0 - empty string --> reached EOF
# -1 - string is NOT in our ENCRYPTED format
#  1 - string is in our ENCRYPTED format
#**********************************************************************
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
#----------------------------------------------------------------------
# RETURN:
#  0 - entire process successful
# -1 - entire process terminated due to file being an invalid ENCYPTED format
#**********************************************************************
def mainSequence( keyCode, OriginFileName, DestinationFileName, mode ):

	# Open the files for READING & WRITING
	OriginFile = open(OriginFileName,'r')
	DestinationFile = open(DestinationFileName,'w') 
	error_flag=0
	print("-------------------------------------------------------")

	#------------------------------------------------------------------
	# ENCRYPTION Sequence
	#------------------------------------------------------------------
	if mode==1:
		while True:
			tmpString = OriginFile.readline()

			# Breaks when read EOF
			if tmpString=="":
				break

			# ENCRYPT string & write to output file
			processedString = encryptThisString(tmpString,keyCode)
			DestinationFile.write(processedString)
	#------------------------------------------------------------------
	# DECRYPTION Sequence
	#------------------------------------------------------------------
	else:
		while True:
			# Identifies the class of the original string by extracting the first 6 bytes
			readString =  OriginFile.read(6)

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