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

#----------------------------------------------------------------------
# Approach :
# - Decided to just stick w/ Tkinter as the GUI framework for this project >_<
# - The UI will be really simple & straight forward to use (refer to mockup!)
# -> [CLASS] InputFileWidget: 
# 		- filename entry field
# 		- icon beside the entry field to open the fileDialog window
# -> [CLASS] KeyWidget
# 		- Customized image label "KEY"
# 		- KEY value entry field 
# -> [CLASS] USBWidget
# 		1. Obtain inital list of USB VID PID 
# 		2. Prompt user to insert USB device (via msgBox)
# 		3. Obtain final list of USB VID PID 
# -> [CLASS] StartWidget
# 		- Button to execute the entire programming sequence (spawn a new thread for task)
# 		- Button to toggle between the 2 modes (change the icon & binding of the other button)
#----------------------------------------------------------------------

#**********************************************************************
# [CLASS] InputFileWidget:
# 	- (Entry) entryField for file directory
# 	- (Label) inputFileButton to open the fileDialog window
#**********************************************************************
class InputFileWidget(tk.Frame):
	# Configure Text & Cursor Color [Class Variable]
	entryBgColor = "#181A15"
	entryTextColor = "#FFFFFF"

	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)

		# Initialize button icons
		self.ButtonImage = tk.PhotoImage(file="selectFile.png")

		# Create an EntryField & Label (pseudoButton) Widget
		self.entryField = tk.Entry(self,font="Verdana 13",width=55,bg=InputFileWidget.entryBgColor,fg=InputFileWidget.entryTextColor,
										insertbackground=InputFileWidget.entryTextColor,highlightthickness=0,borderwidth=0)
		self.inputFileButton = tk.Label(self,image=self.ButtonImage,borderwidth=0,bg="#181A15")

		# Pack the 2 Widgets into a frame
		self.entryField.pack(side=LEFT)
		self.inputFileButton.pack(side=RIGHT)
		self.enable()
	# Check if file can be opened
	def checkFile(self):
		try:
			filePointer = open(self.entryField.get(),'r')
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
			self.entryField.insert(0,file_path)
		# Enable + bind events to sub-widgets
		self.entryField.config(state = tk.NORMAL)
		self.inputFileButton.config(state = tk.NORMAL)
		self.inputFileButton.bind("<Enter>", hoverButton)
		self.inputFileButton.bind("<Leave>", unhoverButton)
		self.inputFileButton.bind("<Button-1>", clickButton )
#**********************************************************************
# [CLASS] KeyWidget:
# 	- (Entry) entryField for KEY
#	  		  Auto-checks if the input value is in the right KEY format
# 	- (Label) keyLabel for KEY icon for UI
#	- (Label) statusLabel displays status messages/instructions
#	- (Label) paddingLabel for padding LOL
#**********************************************************************
class KeyWidget(tk.Frame):

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
		self.entryField = tk.Entry(self,textvariable=self.keyValue,font="Verdana 13",width=10,bg=KeyWidget.entryBgColor,fg=KeyWidget.entryTextColor,
									insertbackground=KeyWidget.entryTextColor,highlightthickness=0,borderwidth=0,show=KeyWidget.bullet)
		self.bottomPadding = tk.Label(self,text="                         ",font="Verdana 13",bg="#272282",borderwidth=0,highlightthickness=0)
		self.statusLabel = tk.Label(self,text="",font="Verdana 8",bg="#123456",fg=KeyWidget.entryTextColor, justify=LEFT,highlightthickness=0)		

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
			self.entryField.config(bg=KeyWidget.entryBgColor)
		else:
			self.statusLabel.config(text="Only numeric characters are allowed!")
			self.entryField.config(bg=KeyWidget.entryBgErrorColor)
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
# [CLASS] USBWidget:
# 	- (Label) statusLabel displays status messages/instructions
#	- (Label) statusLabel to contain Image for UI
#	- (Label) button for registering USB device
#**********************************************************************
class USBWidget(tk.Frame):

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
		self.button = tk.Label(self,text=" + ",bg=USBWidget.unhoverColor)

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
		self.button.config(bg=USBWidget.unhoverColor)
	# Method for enabling widget		
	def enable(self):
		# Define events for the pseudoButton
		def hoverButton(event):		event.widget.config(bg=USBWidget.hoverColor)
		def unhoverButton(event):	event.widget.config(bg=USBWidget.unhoverColor)
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
# class StartWidget(tk.Frame):
		
#*******************************************************************************
# TestBench...
#*******************************************************************************
if __name__ == "__main__":

	root = tk.Tk()                            		#Create app
	root.geometry( "800x400" )						# Set dimensions in pixels
	root.config( bg="#272822")
	EntryWidget = InputFileWidget(root)
	KeyingWidget = KeyWidget(root)
	EntryWidget.place(x=70,y=200)
	KeyingWidget.place(x=70,y=250)
	root.mainloop()

