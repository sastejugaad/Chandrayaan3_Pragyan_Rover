import RPi.GPIO as gpio
import sys
import time
from tkinter import *
from PIL import Image, ImageTk


import bluetooth

#Look for all Bluetooth devices
#the computer knows about.
print ("Searching for devices...")
print ("")
#Create an array with all the MAC
#addresses of the detected devices
nearby_devices = bluetooth.discover_devices()
#Run through all the devices found and list their name
num = 0
print ("Select your device by entering its coresponding number...")
for i in nearby_devices:
	num+=1
	print (num , ": " , bluetooth.lookup_name( i ))


#Allow the user to select their Arduino
#bluetooth module. They must have paired
#it before hand.
selection = int(input("> ")) - 1
print ("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]

port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        #self.showImg()
        

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        maston = Button(self, text="Mast ON", command=self.client_exit)
        mastoff = Button(self, text="Mast Off", command=self.client_exitoff)
        

        # placing the button on my window
        maston.place(x=0, y=0)
        mastoff.place(x=0, y=40)
       
    def showImg(self):
        load = Image.open("chat.png")
        render = ImageTk.PhotoImage(load)
        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()
    def client_exit(self):
        data = "W"
        sock.send(data)
    def client_exitoff(self):
        data = "U"
        sock.send(data)
        #exit()

def key_input(event):
    #init()
    #print 'Key:', event.char
    key_press = event.char
    sleep_time = 0.030
    

    if key_press.lower() == 'w':
        data = "f"
        sock.send(data)
    elif key_press.lower() == 's':
        data = "b"
        sock.send(data)
    elif key_press.lower() == 'a':
        data = "l"
        sock.send(data)
    elif key_press.lower() == 'd':
        data = "r"
        sock.send(data)
    elif key_press.lower() =='X':
        data = "X"
        sock.send(data)
    elif key_press.lower() == 'x':
        data = "x"
        sock.send(data)
    elif key_press.lower() == 'j':
        data = "S"
        sock.send(data)
        
    
        


root = Tk()
root.geometry("800x600")
app = Window(root)
root.bind('<KeyPress>', key_input)
root.mainloop()

