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
	# Method for disabling widget
	def disable(self):
		# Disable + unbind events to sub-widgets
		self.entryField.config(state = tk.DISABLED)
		self.inputFileButton.config(state = tk.DISABLED)
		self.inputFileButton.unbind("<Enter>")
		self.inputFileButton.unbind("<Leave>")
		self.inputFileButton.unbind("<Button-1>")
	# Method for enabling widget
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
# 	- (Label) keyLabel for KEY icon
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

		# Pack the 2 Widgets into a frame
		# self.statusLabel.pack(side=TOP)
		# self.keyLabel.pack(side=LEFT)
		# self.bottomPadding.pack(side=RIGHT)
		# self.entryField.pack(side=RIGHT)
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

# Click me after inserting USB device [red]
# Remove USB Device & try again [red]
# USB device registered! [green]
# Make the text a vector image with holes, then just change frame color when mouse hovers over...
class USBWidget(tk.Frame)

	hoverColor = "#123456"
	unhoverColor = "#123456"

	def __init__(self,parent):
	# Initialize a Frame to group the InputFile Widgets together
	tk.Frame.__init__(self, parent)

	# Initialize variable to track the state machine...
	self.state = 1

	# Create a pseudo Button
	self.button = tk.Label(self)#,image=self.keyImage,borderwidth=0)
	self.button.pack()

	# Define events for the pseudoButton
	def hoverButton(event):
		# if state = 1: 	event.widget.config(image=self.hoverImage1)
		# elif state = 2: event.widget.config(image=self.hoverImage2)
		# else: 			event.widget.config(image=self.hoverImage3)
		event.widget.config(bg=hoverColor)

	def unhoverButton(event):
		event.widget.config(bg=unhoverColor)

	def clickButton(event):
		myFileTypes = [ ('Text Files','*.txt') ]
		# Creates a windows dialog to get user to choose a file to encrypt/decrypt
		file_path = filedialog.askopenfilename(filetypes=myFileTypes, title="Select a file to encrypt/decrypt" )
		self.entryField.insert(0,file_path)

	# Bind the events to the pseudoButton
	self.button.bind("<Enter>", hoverButton)
	self.button.bind("<Leave>", unhoverButton)
	self.button.bind("<Button-1>", clickButton )


class StartWidget(tk.Frame):

	# Configure Text & Cursor Color [Class Variable]
	entryBgColor = "#181A15"
	entryTextColor = "#FFFFFF"

	def __init__(self,parent):
		# Initialize a Frame to group the InputFile Widgets together
		tk.Frame.__init__(self, parent)

		# MODE 1 = ENCRYPT, MODE 0 = DECRYPT
		self.Mode = 1

		# Initialize button icons
		self.hoverToggleImage   = tk.PhotoImage(file="selectFile_hover.png")
		self.unhoverToggleImage = tk.PhotoImage(file="selectFile_unhover.png")
		self.hoverStartImage0    = tk.PhotoImage(file="selectFile_hover.png")
		self.unhoverStartImage0  = tk.PhotoImage(file="selectFile_unhover.png")
		self.hoverStartImage1    = tk.PhotoImage(file="selectFile_hover.png")
		self.unhoverStartImage1  = tk.PhotoImage(file="selectFile_unhover.png")

		# Create an EntryField & Label (pseudoButton) Widget
		self.toggleButton = tk.Label(self,image=self.hoverToggleImage1,borderwidth=0)
		self.startButton  = tk.Label(self,image=self.hoverStartImage1,borderwidth=0)

		# Pack the 2 Widgets into a frame
		self.entryField.pack(side=LEFT)
		self.inputFileButton.pack(side=RIGHT)

		# Define events for the ToggleButton
		def hoverToggleButton(event):
			event.widget.config(image=self.hoverImage)
		def unhoverToggleButton(event):
			event.widget.config(image=self.unhoverImage)
		def clickToggleButton(event):
			if self.mode == 1:
				self.mode == 0
				self.startButton.config(image=self.hoverToggleImage0)
			else:
				self.mode == 1
				self.startButton.config(image=self.hoverToggleImage1)

		# Define events for the StartButton
		def hoverStartButton(event):
			if self.mode == 1:	event.widget.config(image=self.hoverImage1)
			else:				event.widget.config(image=self.hoverImage0)
		def unhoverStartButton(event):
			if self.mode == 1:	event.widget.config(image=self.unhoverImage1)
			else:				event.widget.config(image=self.unhoverImage0)
		def clickStartButton(event):
			print("START!!")

		# Bind the events to the pseudoButton
		self.toggleButton.bind("<Enter>", hoverToggleButton)
		self.toggleButton.bind("<Leave>", unhoverToggleButton)
		self.toggleButton.bind("<Button-1>", clickToggleButton)
		self.startButton.bind("<Enter>", hoverStartButton)
		self.startButton.bind("<Leave>", unhoverStartButton)
		self.startButton.bind("<Button-1>", clickStartButton)

	def disable(self):
		self.toggleButton.config(state = tk.DISABLED)
		self.startButton.config(state = tk.DISABLED)
		# disable bg color...

		
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

