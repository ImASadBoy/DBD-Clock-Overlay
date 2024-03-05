import tkinter as tk
from PIL import ImageTk, Image, ImageGrab
import time
import keyboard
from easyocr import Reader
from map_find_logic import *
import configparser

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()


def grab():
    # Capture the entire screen
    screenshot = ImageGrab.grab(bbox=(0, (height/3)*2, width, height))
    screenshot.save("assets/temp/screen.png")
    # Save the screenshot to a file
    screenshot.close()
    config = configparser.ConfigParser()
    config.read("config/settings.ini")
    # Close the screenshot

    map, realm = map_logic()
    
    if map:
        if realm:    
            return ("assets/" + config["gui"]["variation"] + "/" + map, realm, "assets/" + config["gui"]["variation"] + "/")
        else:
            return ("assets/" + config["gui"]["variation"] + "/" + map, 0, "assets/" + config["gui"]["variation"] + "/")
    else:
        return ("assets/others/failed_map.png", 0, 0)
    # Carica l'immagine
    # Crea un lettore OCR
    

