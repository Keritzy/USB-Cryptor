# USBCRYPTOR
Textfile encryptor/decryptor made with Python 3 & Tkinter UI Framework

![ScreenShot](resources/images/screenshot.png)
[Download the executable here!](https://www.dropbox.com/s/83xbkz0vci07vub/USBCRYPTOR_setup_v1.3.exe?dl=0) (Made w/ py2exe & Inno Setup Compiler)

How it works?
-------
+ When user registers a USB device, the program detects if there's any new device connected to the PC.
+ A function then retrieves the details of this new USB device (via the win32com module) & extracts its Vendor & Product ID (VID & PID).
+ An 8-digit KEY chosen by the user & the devices's PID/VID will be used for encryption/decryption algorithm.

How to Encrypt a .txt file:
-------
1. Choose the textfile that you want to encrypt by clicking on the magnifying glass icon
2. Enter a 8-digit numeric KEY
3. Register your USB Flashdrive
4. Toggle & select encryption mode
5. Click on ENCRYPT

How to Decrypt a .txt file:
-------
1. Choose the textfile that you want to decrypt by clicking on the magnifying glass icon
2. Enter the 8-digit numeric KEY used for the encryption process
3. Register your USB Flashdrive used for the encryption process
4. Toggle & select decryption mode
5. Click on DECRYPT

Limitations:
-------
+ Only able to process ASCII, any .txt files with other encodings (eg. UTF-8 etc.) will cause it to fail
