#!/usr/bin/python
import tkinter as tk
from tkinter import *

from resources.classes import FileInputWidget
from resources.classes import KeyInputWidget
from resources.classes import RegisterUsbWidget 
from resources.classes import StartProgramWidget

import win32com.client

if __name__ == "__main__":

	root = tk.Tk()                      			# Create app
	root.iconify()									# Hide UI window to let the program load all the objects on the UI
	root.iconbitmap("resources/images/icon.ico")	#Add Icon to GUI window
	root.geometry( "800x500" )						# Set dimensions in pixels
	root.wm_title("USBCRYPTOR")    				# Add title to GUI window
	root.resizable(0,0)								# Make the Window not resizable

	# Add in the background for the UI
	backgroundImage = tk.PhotoImage(file="resources/images/background.png")
	background = tk.Label(root,image=backgroundImage,borderwidth=0,highlightthickness=0)
	background.place(x=0,y=0,relwidth=1,relheight=1)

	# Create UI objects
	A = FileInputWidget(root)
	B = KeyInputWidget(root)
	C = RegisterUsbWidget(root)
	D = StartProgramWidget(root,A,B,C)

	# Place them in the tkinter Window
	A.place(x=83,y=297)
	B.place(x=83,y=330)
	C.place(x=83,y=379)
	D.place(x=486,y=328)
	root.deiconify()								# Done loading all the object, un-hide UI window
	root.mainloop()