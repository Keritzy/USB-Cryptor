#!/usr/bin/python
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import resources.encryption_Functions as encrypt
import resources.usb_Functions as usb

#----------------------------------------------------------------------
# Main Objective:
# Create classes for widgets since they're going to be heavily customized to look
# modern & non-native...
#----------------------------------------------------------------------
class Color():

	# Define class variables -> meant to be global COLOR constants
	entryBg    	= "#181A15"
	entryText 	= "#FFFFFF"
	bgColor 	= "#272822"
	skyblue		= "#0080FF"
	amber		= "#FEAC01"
	red 		= "#ED1C24"
	green		= "#22B14C"
	grey 		= "#494949"

	bullet = "\u2022" 				#specifies bullet character

	def __init__():
		pass

#**********************************************************************
# [CLASS] FileInputWidget:
#   - Inherits the Color Class
# 	- (Entry) entryField => Display selected file directory
# 	- (Label) inputFileButton => open the fileDialog window
#**********************************************************************
class FileInputWidget(tk.Frame, Color):
	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)

		# Initialize button icons
		self.ButtonImage = tk.PhotoImage(file="resources/images/FileInput_Icon.png")

		# Set up tracing for entryField...
		self.filePath = StringVar()
		self.filePath.trace("w", self.autoCheck)

		# Create an EntryField & Label (pseudoButton) Widget
		self.entryField = tk.Entry(self,borderwidth=0,textvariable=self.filePath,font="Verdana 13",width=55,
										bg=Color.entryBg,fg=Color.entryText,insertbackground=Color.entryText)
		self.inputFileButton = tk.Label(self,borderwidth=0,image=self.ButtonImage,bg=Color.red)

		# Pack the 2 Widgets into a frame
		self.entryField.pack(side=LEFT)
		self.inputFileButton.pack(side=RIGHT)
		self.enable()

	# Method for TRACING entryField
	def autoCheck(self,*args):
		if self.checkValue() == 0:	self.inputFileButton.config(bg=Color.green)
		else:						self.inputFileButton.config(bg=Color.red)

	# Checks if file can be opened
	def checkValue(self):
		try:
			tmp = self.entryField.get()
			filePointer = open(tmp,'r')
		except Exception:
		    return -1

		filePointer.close()
		return 0

	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.entryField.get()

	# Method for enabling the CLASS widget
	def enable(self):

		# Define events for the pseudoButton
		def hoverButton(event):	
			event.widget.config(bg=Color.skyblue)

		def unhoverButton(event):	
			if self.checkValue() == 0:	event.widget.config(bg=Color.green)
			else:						event.widget.config(bg=Color.red)

		# Creates a windows dialog to get user to choose a file to encrypt/decrypt
		def clickButton(event):		
			file_path = filedialog.askopenfilename(filetypes=[ ('Text Files','*.txt') ], title="Select a file to encrypt/decrypt" )
			if file_path!="":
				self.entryField.delete(0,END)
				self.entryField.insert(0,file_path)

			if self.checkValue() == 0:	event.widget.config(bg=Color.green)
			else:						event.widget.config(bg=Color.red)

		# bind events to sub-widgets
		self.inputFileButton.bind("<Enter>", hoverButton)
		self.inputFileButton.bind("<Leave>", unhoverButton)
		self.inputFileButton.bind("<Button-1>", clickButton )
#**********************************************************************
# [CLASS] KeyInputWidget:
#   - Inherits the Color Class
# 	- (Entry) entryField => display KEY values
#	  		  Auto-checks if the input value is in the right KEY format
# 	- (Label) keyLabel => KEY icon for UI
#	- (Label) statusLabel => displays status messages/instructions
#	- (Label) bottomPadding => for UI layout purposes
#**********************************************************************
class KeyInputWidget(tk.Frame,Color):
	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.config(bg=Color.bgColor)									# Set Frame color to match UI background
		self.keyImage = tk.PhotoImage(file="resources/images/KeyInput_Icon.png")	# Initialize button icons
		
		# Set up tracing for KEY entryField...
		self.keyValue = StringVar()
		self.keyValue.trace("w", self.autoCheck)

		# Create an EntryField & label (icon) Widget
		self.keyLabel = tk.Label(self,borderwidth=0,image=self.keyImage,bg=Color.red)
		self.statusLabel = tk.Label(self,text="",font="Verdana 8",bg=Color.bgColor,fg=Color.entryText)
		self.entryField = tk.Entry(self,borderwidth=0,textvariable=self.keyValue,font="Verdana 14",width=13,
										bg=Color.entryBg,fg=Color.entryText,insertbackground=Color.entryText,
										justify=CENTER,show=Color.bullet)
		self.bottomPadding = tk.Label(self,borderwidth=0,text="                 ",font="Verdana 13",bg=Color.bgColor)
				

		self.statusLabel.grid(row=0,column=1,columnspan=2,sticky=W,pady=3)
		self.keyLabel.grid(row=1,column=0)
		self.entryField.grid(row=1,column=1)
		self.bottomPadding.grid(row=1,column=2)

	def autoCheck(self,*args):
		# Limits the entryField to allow up to 8-chars
		tmp_string = self.keyValue.get()
		tmp_length = len(tmp_string)
		if len(tmp_string) > 8 :
			self.entryField.delete(tmp_length-1,tmp_length)

		# Changes icon to GREEN if key passes the checkValue()
		if self.checkValue()==0:
			self.statusLabel.config(text="")	
			self.keyLabel.config(bg=Color.green)
		# Changes icon to RED + outputs msg to user if input is non-numeric	
		else:
			if not (tmp_string).isdigit():	self.statusLabel.config(text="Only numeric characters are allowed!")	
			else:							self.statusLabel.config(text="")
			self.keyLabel.config(bg=Color.red)

	# Method to check wether the value contained EntryField is an 8-digit number
	def checkValue(self):
		if len(self.keyValue.get())==8 and (self.keyValue.get()).isdigit():	return 0
		else:															    return -1

	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.entryField.get()
#**********************************************************************
# [CLASS] RegisterUsbWidget:
#   - Inherits the Color Class
# 	- (Label) statusLabel => displays status messages/instructions
#	- (Label) statusImage => contain Image for UI
#	- (Label) button => click to register USB device
#	- (Label) bottomPadding => for UI layout purposes
#**********************************************************************
class RegisterUsbWidget(tk.Frame,Color):
	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.state = 1								# STATE variable to track current STATE
		self.oldDeviceList = ""
		self.newDeviceList = ""
		self.usbIdValue = ""
		self.config(bg=Color.bgColor)

		# Initialize Images & Icons
		self.buttonImage1 = tk.PhotoImage(file="resources/images/RegisterUsb_Button1.png")
		self.buttonImage2 = tk.PhotoImage(file="resources/images/RegisterUsb_Button2.png")
		self.stateImage1  = tk.PhotoImage(file="resources/images/RegisterUsb_State1.png")
		self.stateImage2  = tk.PhotoImage(file="resources/images/RegisterUsb_State2.png")
		self.stateImage3  = tk.PhotoImage(file="resources/images/RegisterUsb_State3.png")

		# Create a pseudo Button
		self.statusLabel = tk.Label(self, text="",bg=Color.bgColor,fg=Color.entryText)
		self.statusImage = tk.Label(self, image=self.stateImage1,borderwidth=0,highlightthickness=0)
		self.button = tk.Label(self, image=self.buttonImage1,bg=Color.red,borderwidth=0,highlightthickness=0)
		self.bottomPadding = tk.Label(self,text="            ",font="Verdana 13",bg=Color.bgColor,borderwidth=0,highlightthickness=0)
		
		# Pack the widgets into the Frame
		self.statusLabel.grid(row=0,column=0,columnspan=4,sticky=W) 
		self.button.grid(row=1,column=2,sticky=N)
		self.statusImage.grid(row=1,rowspan=2,column=0) 
		self.bottomPadding.grid(row=1,rowspan=2,column=3) 
		self.enable()

	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.usbIdValue
	
	# Method to check if USB is registered
	def checkValue(self):
		if self.state==3:	return 0
		else: 				return -1

	# Method for enabling widget		
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):		event.widget.config(bg=Color.skyblue)
	
		def unhoverButton(event):
			if self.state==1:	self.button.config(image=self.buttonImage1,bg=Color.red)
			elif self.state==2: self.button.config(image=self.buttonImage2,bg=Color.amber)
			else:				self.button.config(image=self.buttonImage1,bg=Color.green)
	
		def clickButton(event):
			if (self.state==1) or (self.state==3):
				self.oldDeviceList = usb.getDeviceIDList()
				self.statusLabel.config(text="                        Insert USB device & click \u2714")
				self.statusImage.config(image=self.stateImage2)
				self.button.config(image=self.buttonImage2,bg=Color.amber)
				self.state = 2
				return
			else:
				self.newDeviceList = usb.getDeviceIDList()
				tmpDeviceString = usb.getNewDeviceID(self.oldDeviceList,self.newDeviceList)
				if tmpDeviceString != "ERROR":
					self.usbIdValue = usb.extractID(tmpDeviceString)
					self.statusLabel.config(text="")
					self.statusImage.config(image=self.stateImage3)
					self.button.config(image=self.buttonImage1,bg=Color.green)
					self.state = 3
				else:
					self.statusLabel.config(text="                        [FAILED] Remove USB device & try again...")
					self.statusImage.config(image=self.stateImage1)
					self.button.config(image=self.buttonImage1,bg=Color.red)
					self.state = 1

		# Bind events to sub-widgets
		self.button.bind("<Enter>", hoverButton)
		self.button.bind("<Leave>", unhoverButton)
		self.button.bind("<Button-1>", clickButton )

#**********************************************************************
# [CLASS] StartProgramWidget:
#   - Inherits the Color Class
# 	- (Label) toggleButton => toggle between encryption/decryption mode
#	- (Label) startButton => execute encrypt/decrypt sequence
#**********************************************************************
class StartProgramWidget(tk.Frame,Color):
	def __init__(self,parent,FileInputObject,KeyInputObject,RegisterUsbObject):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.state = 1								# STATE variable to track current STATE
		self.FileInputObject   = FileInputObject
		self.KeyInputObject    = KeyInputObject
		self.RegisterUsbObject = RegisterUsbObject

		# Initialize Images & Icons
		self.toggleEncryptImage = tk.PhotoImage(file="resources/images/StartProgram_ToggleEncrypt.png")
		self.toggleDecryptImage = tk.PhotoImage(file="resources/images/StartProgram_ToggleDecrypt.png")
		self.encryptImage = tk.PhotoImage(file="resources/images/StartProgram_Encrypt.png")
		self.decryptImage = tk.PhotoImage(file="resources/images/StartProgram_Decrypt.png")

		# Create a pseudo Button
		self.toggleButton = tk.Label(self,image=self.toggleEncryptImage,bg=Color.grey,borderwidth=0)
		self.startButton  = tk.Label(self,image=self.encryptImage,bg=Color.entryBg,borderwidth=0)

		# Pack the widgets into the Frame
		self.toggleButton.grid(row=0,column=0)
		self.startButton.grid(row=0,column=1)
		self.enable()

	# Method for enabling widget		
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):			
			# Series of checks before executing the encryption/decryption sequence
			if(self.FileInputObject.checkValue()   == 0 and
			   self.KeyInputObject.checkValue()    == 0 and
		 	   self.RegisterUsbObject.checkValue() == 0):
				self.startButton.config(bg=Color.green)
			else:
				self.startButton.config(bg=Color.red)
		def unhoverButton(event):		event.widget.config(bg=Color.entryBg)
		def hoverToggleButton(event):	event.widget.config(bg=Color.skyblue)
		def unhoverToggleButton(event):	event.widget.config(bg=Color.grey)
		def clickToggleButton(event):
			if self.state==1:
				self.state=2
				self.toggleButton.config(image=self.toggleDecryptImage)
				self.startButton.config(image=self.decryptImage)
			else:
				self.state=1
				self.toggleButton.config(image=self.toggleEncryptImage)
				self.startButton.config(image=self.encryptImage)

		def clickStartButton(event):
			# Series of checks before executing the encryption/decryption sequence
			if self.FileInputObject.checkValue() == -1:   return
			if self.KeyInputObject.checkValue() == -1: 	  return
			if self.RegisterUsbObject.checkValue() == -1: return

			# Lock in values before executing the encryption/decryption sequence
			originFileName = self.FileInputObject.getValue()		
			KeyString 	 = self.KeyInputObject.getValue()
			UsbString 	 = self.RegisterUsbObject.getValue()

			# Generate Master KEY for ENCRYPTION/DECRYPTION
			keyCode = UsbString+KeyString
			encrypt.mainSequence(keyCode,originFileName,self.state)

		# Enable + bind events to sub-widgets
		self.toggleButton.bind("<Enter>",hoverToggleButton)
		self.toggleButton.bind("<Leave>",unhoverToggleButton)
		self.toggleButton.bind("<Button-1>",clickToggleButton)
		self.startButton.bind("<Enter>",hoverButton)
		self.startButton.bind("<Leave>",unhoverButton)
		self.startButton.bind("<Button-1>",clickStartButton)