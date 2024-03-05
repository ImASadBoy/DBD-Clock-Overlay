import configparser
from tkinter import *
from tkinter.ttk import *
import customtkinter as ctk
import keyboard
from grab_screen import *
import configparser

config = configparser.ConfigParser()
config.read("config/settings.ini")
sett = config.sections()

def updateConfig(param, value):
  config["DEFAULT"][param] =  str(value)
  with open('config/settings.ini', 'w') as configfile:
    config.write(configfile)
  
def updateKeybinds(param, value):
  config["keybinds"][param] =  str(value).replace("'", "")
  with open('config/settings.ini', 'w') as configfile:
    config.write(configfile)

'''
def keyWindow(master, keybind, winwidth, winheight, winx, winy):
     
    print(master, keybind)
    # Toplevel object which will 
    # be treated as a new window
    newWindow = ctk.CTkToplevel(master)
    newWinsize = round(int(winheight)/3)
    newWindowX = int(winx) + round((int(winwidth) - newWinsize)/2)
    newWindowY = int(winy) + round((int(winheight) - newWinsize)/2)
    newWindowgeo = str(newWinsize) + "x" + str(newWinsize) + "+" + str(newWindowX) + "+" + str(newWindowY)
    # sets the title of the
    # Toplevel widget
    print(newWinsize, newWindowX, newWindowY, newWindowgeo)
    newWindow.title("Press a key to remap")
 
    # sets the geometry of toplevel
    newWindow.geometry(newWindowgeo)
 
    # A Label widget to show in toplevel
    ctk.CTkLabel(newWindow, text ="press a key").pack()
    newWindow.attributes('-topmost',True)
    newWindow.update()
    k = keyboard.read_key()
    config["keybinds"][keybind] = "Key." + str(k)
    with open('config/settings.ini', 'w') as configfile:
        config.write(configfile)
    newWindow.destroy()
'''

def updateVersion(*args):
  if config["gui"]["variation"] == "original":
    variation = "alternate"
  else:
    variation = "original"
  config["gui"]["variation"] = variation
  with open('config/settings.ini', 'w') as configfile:
    config.write(configfile)