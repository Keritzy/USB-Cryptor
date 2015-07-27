#!/usr/bin/python
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import threading

import encryption_Functions as encrypt
import usb_Functions as usb

# import resources.encryption_Functions as encrypt
# import resources.usb_Functions as usb

#----------------------------------------------------------------------
# Main Objective:
# Create classes for widgets since they're going to be heavily customized to look
# modern & non-native...
#----------------------------------------------------------------------

#**********************************************************************
# [CLASS] FileInputWidget:
# 	- (Entry) entryField for file directory
# 	- (Label) inputFileButton to open the fileDialog window
#**********************************************************************
class FileInputWidget(tk.Frame):
	# Configure Text & Cursor Color [Class Variable]
	entryBgColor = "#181A15"
	entryTextColor = "#FFFFFF"

	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)

		# Initialize button icons
		self.ButtonImage = tk.PhotoImage(file="selectFile.png")

		# Create an EntryField & Label (pseudoButton) Widget
		self.entryField = tk.Entry(self,font="Verdana 13",width=55,bg=FileInputWidget.entryBgColor,fg=FileInputWidget.entryTextColor,
										insertbackground=FileInputWidget.entryTextColor,highlightthickness=0,borderwidth=0)
		self.inputFileButton = tk.Label(self,image=self.ButtonImage,borderwidth=0,bg="#181A15")

		# Pack the 2 Widgets into a frame
		self.entryField.pack(side=LEFT)
		self.inputFileButton.pack(side=RIGHT)
		self.enable()
	# Check if file can be opened
	def checkValue(self):
		try:
			tmp = self.entryField.get()
			filePointer = open(tmp,'r')
		except Exception:
		    return -1                               	# returns "ERROR" to abort process...

		filePointer.close()
		return 0	
	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.entryField.get()
	# Method for disabling the CLASS widget
	def disable(self):
		# Disable + unbind events to sub-widgets
		self.entryField.config(state = tk.DISABLED)
		self.inputFileButton.config(state = tk.DISABLED)
		self.inputFileButton.unbind("<Enter>")
		self.inputFileButton.unbind("<Leave>")
		self.inputFileButton.unbind("<Button-1>")
	# Method for enabling the CLASS widget
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):		event.widget.config(bg="#FFFFFF")
		def unhoverButton(event):	event.widget.config(bg="#181A15")
		# Creates a windows dialog to get user to choose a file to encrypt/decrypt
		def clickButton(event):		
			file_path = filedialog.askopenfilename(filetypes=[ ('Text Files','*.txt') ], title="Select a file to encrypt/decrypt" )
			if file_path!="":
				self.entryField.delete(0,END)
				self.entryField.insert(0,file_path)
		# Enable + bind events to sub-widgets
		self.entryField.config(state = tk.NORMAL)
		self.inputFileButton.config(state = tk.NORMAL)
		self.inputFileButton.bind("<Enter>", hoverButton)
		self.inputFileButton.bind("<Leave>", unhoverButton)
		self.inputFileButton.bind("<Button-1>", clickButton )
#**********************************************************************
# [CLASS] KeyInputWidget:
# 	- (Entry) entryField for KEY
#	  		  Auto-checks if the input value is in the right KEY format
# 	- (Label) keyLabel for KEY icon for UI
#	- (Label) statusLabel displays status messages/instructions
#	- (Label) paddingLabel for padding LOL
#**********************************************************************
class KeyInputWidget(tk.Frame):

	# Configure Text & Cursor Color [Class Variable]
	entryBgColor 		= "#181A15"
	entryBgErrorColor 	= "#FF0000"
	entryTextColor 		= "#FFFFFF"
	bullet = "\u2022" 				#specifies bullet character

	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.config(bg="#272822")			# Set Frame color to match UI background

		# Initialize button icons
		self.keyImage = tk.PhotoImage(file="selectFile_hover.png")
		
		# Set up tracing for KEY entryField...
		self.keyValue = StringVar()
		self.keyValue.trace("w", self.checkKey)
		
		# Create an EntryField & label (icon) Widget
		self.keyLabel = tk.Label(self,image=self.keyImage,borderwidth=0)
		self.entryField = tk.Entry(self,textvariable=self.keyValue,font="Verdana 13",width=10,bg=KeyInputWidget.entryBgColor,fg=KeyInputWidget.entryTextColor,
									insertbackground=KeyInputWidget.entryTextColor,highlightthickness=0,borderwidth=0,show=KeyInputWidget.bullet)
		self.bottomPadding = tk.Label(self,text="                         ",font="Verdana 13",bg="#272282",borderwidth=0,highlightthickness=0)
		self.statusLabel = tk.Label(self,text="",font="Verdana 8",bg="#123456",fg=KeyInputWidget.entryTextColor, justify=LEFT,highlightthickness=0)		

		self.statusLabel.grid(row=0,column=1,columnspan=2,sticky=W,pady=3)
		self.keyLabel.grid(row=1,column=0)
		self.entryField.grid(row=1,column=1)
		self.bottomPadding.grid(row=1,column=2)

		# # Debugging button---------------------
		# def thislor():
		# 	print(self.entryField.get())	
		# button = Button(self, text="click me", command=thislor )
		# button.pack()
		# #--------------------------------------

	def checkKey(self,*args):
		tmp_string = self.keyValue.get()
		tmp_length = len(tmp_string)
		if tmp_length > 8 :
			self.entryField.delete( tmp_length-1,tmp_length)

		if (tmp_string).isdigit() or tmp_string == "":
			self.statusLabel.config(text="")
			self.entryField.config(bg=KeyInputWidget.entryBgColor)
		else:
			self.statusLabel.config(text="Only numeric characters are allowed!")
			self.entryField.config(bg=KeyInputWidget.entryBgErrorColor)
	def checkValue(self):
		if len(self.keyValue.get())==8 and (self.keyValue.get()).isdigit():	return 0
		else:							 									return -1
	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.entryField.get()
	# Method for disabling the CLASS widget
	def disable(self):
		self.entryField.config(state = tk.DISABLED)
	# Method for enabling the CLASS widget
	def enable(self):
		self.entryField.config(state = tk.NORMAL)
#**********************************************************************
# [CLASS] RegisterUsbWidget:
# 	- (Label) statusLabel displays status messages/instructions
#	- (Label) statusLabel to contain Image for UI
#	- (Label) button for registering USB device
#**********************************************************************
class RegisterUsbWidget(tk.Frame):

	hoverColor = "#00FFFF"
	unhoverColor = "#181A15"

	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.state = 1								# STATE variable to track current STATE
		self.oldDeviceList = ""
		self.newDeviceList = ""
		self.usbIdValue = ""

		# Create a pseudo Button
		self.statusLabel = tk.Label(self, text="Nothing",bg="#FF0000")
		self.statusImage = tk.Label(self, text="NOT REGISTERED\n",bg="#FF0000")
		self.button = tk.Label(self,text=" + ",bg=RegisterUsbWidget.unhoverColor)

		# Pack the widgets into the Frame
		self.button.grid(row=1,column=1)
		self.statusLabel.grid(row=0,column=0) 
		self.statusImage.grid(row=1,rowspan=2,column=0)  
		self.enable()

	# Method for disabling widget
	def disable(self):
		# Disable + unbind events to sub-widgets
		self.button.unbind("<Enter>")
		self.button.unbind("<Leave>")
		self.button.unbind("<Button-1>")
		self.button.config(bg=RegisterUsbWidget.unhoverColor)
	# Method for enabling widget		
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):		event.widget.config(bg=RegisterUsbWidget.hoverColor)
		def unhoverButton(event):	event.widget.config(bg=RegisterUsbWidget.unhoverColor)
		# 
		def clickButton(event):
			if (self.state==1) or (self.state==3):
				self.oldDeviceList = usb.getDeviceIDList()
				self.statusLabel.config(text="Insert USB device & click \u2714")
				self.statusImage.config(text="REGISTERING\n",bg="#FFFF00")
				self.button.config(text=" \u2714 ")
				self.state = 2
				return
			else:
				self.newDeviceList = usb.getDeviceIDList()
				tmpDeviceString = usb.getNewDeviceID(self.oldDeviceList,self.newDeviceList)
				if tmpDeviceString != "ERROR":
					self.usbIdValue = usb.extractID(tmpDeviceString)
					self.statusLabel.config(text="SUCCESS!")
					self.statusImage.config(text="REGISTERED\n",bg="#00FF00")
					self.button.config(text=" + ")
					self.state = 3
				else:
					self.statusLabel.config(text="[FAILED] Remove USB device & try again...")
					self.statusImage.config(text="NOT REGISTERED\n",bg="#FF0000")
					self.button.config(text=" + ")
					self.state = 1

		# Enable + bind events to sub-widgets
		self.button.bind("<Enter>", hoverButton)
		self.button.bind("<Leave>", unhoverButton)
		self.button.bind("<Button-1>", clickButton )
	# Method to retrieve value contained EntryField
	def getValue(self):
		return self.usbIdValue
	def checkValue(self):
		if self.state==3:	return 0
		else: 				return -1
#**********************************************************************
# [CLASS] StartProgramWidget:
# 	- (Label) toggleButton to toggle between encryption/decryption mode
#	- (Label) startButton to execute encrypt/decrypt sequence
#**********************************************************************
class StartProgramWidget(tk.Frame):

	hoverColor = "#FF0000"
	unhoverColor = "#181A15"

	def __init__(self,parent,FileInputObject,KeyInputObject,RegisterUsbObject):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)
		self.state = 1								# STATE variable to track current STATE
		self.FileInputObject   = FileInputObject
		self.KeyInputObject    = KeyInputObject
		self.RegisterUsbObject = RegisterUsbObject

		# Create a pseudo Button
		self.toggleButton = tk.Label(self, text="Toggle",bg="#FFFFFF",fg="#FFFFFF")
		self.startButton  = tk.Label(self, text="ENCRYPT\n",bg="#00FFFF",fg="#FFFFFF")

		# Pack the widgets into the Frame
		self.toggleButton.grid(row=0,column=0)
		self.startButton.grid(row=0,column=1)
		self.enable()

	# Method for disabling widget
	def disable(self):
		# Disable + unbind events to sub-widgets
		self.toggleButton.unbind("<Enter>")
		self.toggleButton.unbind("<Leave>")
		self.toggleButton.unbind("<Button-1>")
		self.startButton.unbind("<Enter>")
		self.startButton.unbind("<Leave>")
		self.startButton.unbind("<Button-1>")
		# Change set background back to non-hover color
		self.toggleButton.config(bg=StartProgramWidget.unhoverColor)
		self.startButton.config(bg=StartProgramWidget.unhoverColor)
	# Method for enabling widget		
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):		event.widget.config(bg=StartProgramWidget.hoverColor)
		def unhoverButton(event):	event.widget.config(bg=StartProgramWidget.unhoverColor)
		def clickToggleButton(event):
			if self.state==1:
				self.state=2
				self.startButton.config(text="DECRYPT\n",bg="#00FF00")
			else:
				self.state=1
				self.startButton.config(text="ENCRYPT\n",bg="#00FFFF")

		def clickStartButton(event):
			# Series of checks before executing the encryption/decryption sequence
			if self.FileInputObject.checkValue() == -1:
				print( "INVALID FILE")
				return

			if self.KeyInputObject.checkValue() == -1:
				print( "INVALID KEY")
				return

			if self.RegisterUsbObject.checkValue() == -1:
				print( "INVALID USB")
				return

			# Lock in values before executing the encryption/decryption sequence
			originFileName = self.FileInputObject.getValue()		
			KeyString 	 = self.KeyInputObject.getValue()
			UsbString 	 = self.RegisterUsbObject.getValue()

			# Generate Master KEY for ENCRYPTION/DECRYPTION
			keyCode = UsbString+KeyString

			# Creates an empty .txt file with the chosen destinationFileName
			# destinationFileName = filedialog.asksaveasfile(filetypes=[ ('Text Files','*.txt') ], 
			#  												title="Select a file to encrypt/decrypt", defaultextension=".txt")
			
			# Crude method to convert the return value from the fileDialog into a string
			# tmpEntryField = tk.Entry(self)
			# tmpEntryField.insert(0,destinationFileName)
			# destinationFileName = tmpEntryField.get()

			# Check whether it's an encryption or a decryption sequence
			# ENCRYPT(self.state==1) & DECRYPT(self.state==2)
			encrypt.mainSequence(keyCode,originFileName,self.state)
			print("everythingDONE")

		# Enable + bind events to sub-widgets
		self.toggleButton.bind("<Enter>",hoverButton)
		self.toggleButton.bind("<Leave>",unhoverButton)
		self.toggleButton.bind("<Button-1>",clickToggleButton)
		self.startButton.bind("<Enter>",hoverButton)
		self.startButton.bind("<Leave>",unhoverButton)
		self.startButton.bind("<Button-1>",clickStartButton)
		
#*******************************************************************************
# TestBench...
#*******************************************************************************
if __name__ == "__main__":

	root = tk.Tk()                            		#Create app
	root.geometry( "800x400" )						# Set dimensions in pixels
	root.config( bg="#272822")
	A = FileInputWidget(root)
	B = KeyInputWidget(root)
	C = RegisterUsbWidget(root)
	D = StartProgramWidget(root,A,B,C)
	A.place(x=70,y=200)
	B.place(x=70,y=225)
	C.place(x=70,y=280)
	D.place(x=600,y=250)
	root.mainloop()

