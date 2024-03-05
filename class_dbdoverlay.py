import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageGrab
import time
from pynput import keyboard
#from pynput import keyboard as k
from pynput.keyboard import Key, Listener, KeyCode
from grab_screen import *
import configparser
import functools


con = configparser.ConfigParser()

def myround(x, base=5):
    return base * round(x/base)

def do_not_run_twice(func):
    prev_call = None

    @functools.wraps(func) # It is good practice to use this decorator for decorators
    def wrapper(*args, **kwargs):
        nonlocal prev_call

        if (args, kwargs) == prev_call:
            return None
        prev_call = args, kwargs
        return func(*args, **kwargs)

    return wrapper
       

class dbdOverlay:
    
    def __init__(self, master):
        self.master = master
        self.status = ""
        self.config = con.read("config/settings.ini")
        self.toggle_overlay = con["keybinds"]["toggle_overlay"]
        self.take_screenshot = con["keybinds"]["screenshot"]
        self.cycle_map = con["keybinds"]["cycle_map"]
        self.variation = con["gui"]["variation"]
        self.rgba = (con["DEFAULT"]["red"], con["DEFAULT"]["green"], con["DEFAULT"]["blue"], con["DEFAULT"]["alpha"])
        self.addsize = con["DEFAULT"]["addsize"]
        self.sizeX = 450 + int(self.addsize)
        self.sizeY = 500 + int(self.addsize)
        self.position = (con["DEFAULT"]["positionX"], con["DEFAULT"]["positionY"])
        self.map = "assets/others/no_map.png"
        self.assetsPath = "assets/" + con["gui"]["variation"] + "/"
        self.realm = 0
        self.cycle = ""
        #self.image = ImageTk.PhotoImage(resizeImg(self.map, self.size[0], self.size[1]))
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        geo = str(self.sizeX) + "x" + str(self.sizeY)
        self.master.geometry(geo)
        self.master.geometry("+" + con["DEFAULT"]["positionx"] + "+" + con["DEFAULT"]["positiony"])
        self.master.configure(bg='gray')
        self.master.overrideredirect(True)
        img = Image.open(self.map)
        self.image = ImageTk.PhotoImage(img)
        self.panel = tk.Label(self.master, image = self.image)
        self.panel.update_img = self.image
        self.panel.pack(expand = True)
        self.master.attributes("-alpha", float(con["DEFAULT"]["alpha"])/10)
        self.resizeImg()
        
    
    def resizeImg(self):
        img = Image.open(self.map)
        #img_width, img_height = img.size
        #max_scale_width = int(width)/img_width
        #max_scale_height = (int(height) - (int(height)/10))/img_height
        #min_scale = min(max_scale_width, max_scale_height)
        #img = img.resize((int(img_width * min_scale), int(img_height * min_scale)), Image.LANCZOS)
        self.config = con.read("config/settings.ini")
        self.addsize = con["DEFAULT"]["addsize"]
        self.sizeX = 450 + int(self.addsize)
        self.sizeY = 500 + int(self.addsize)
        self.image = ImageTk.PhotoImage(img.resize((self.sizeX, self.sizeY), Image.LANCZOS))
        self.panel.configure(bg='gray')
        self.panel.config(image = self.image)
        self.panel.update_img = self.image
        
        
    def pUpdateMap(self, *dummy):
        current_time = time.strftime("%S")
        self.updateMap(round(int(current_time)/10))
        
    @do_not_run_twice              
    def updateMap(self, sts): 
        self.status = "updating"
        self.map, self.realm, self.assetsPath = grab()
        self.image = self.resizeImg()
        #self.panel.after(6000, self.updateOverlay)
        self.status = ""   
            
    def pCycleMap(self, *dummy):
        current_time = time.strftime("%S")
        self.cycleMap(current_time)
        
    @do_not_run_twice                
    def cycleMap(self, *args):
        if self.realm:
            if self.cycle == "":
                self.map = self.assetsPath + self.realm + "_i.png"
                self.cycle = "_i"
            elif self.cycle == "_i":
                self.map = self.assetsPath + self.realm + "_ii.png"
                self.cycle = "_ii"
            elif self.cycle == "_ii":
                self.map = self.assetsPath + self.realm + ".png"
                self.cycle = ""
            self.image = ImageTk.PhotoImage(self.resizeImg())
            self.panel.config(image = self.image)
            self.panel.update_img = self.image
   
   
    def updateKeys(self, *args):
        self.config = con.read("config/settings.ini")
        self.toggle_overlay = con["keybinds"]["toggle_overlay"]
        self.take_screenshot = con["keybinds"]["screenshot"]
        self.cycle_map = con["keybinds"]["cycle_map"]
        self.variation = con["gui"]["variation"]
        self.listen()                
            
    def makeTopmost(self, *args):
        self.master.wm_attributes("-topmost", True)
        self.master.wm_deiconify()
        self.master.overrideredirect(True)
    
    def removeTopmost(self, *args):
        self.master.wm_attributes("-topmost", False)
        self.master.wm_withdraw()
        self.master.overrideredirect(True)
    
    def on_press(self, key):
        try:
            if key.char == self.toggle_overlay.replace("Key.", ""):
                self.makeTopmost()
            elif key.char == self.take_screenshot.replace("Key.", ""):
                self.pUpdateMap()
            elif key.char == self.cycle_map.replace("Key.", ""):
                self.pCycleMap()
        except:
            if str(key) == self.toggle_overlay:
                self.makeTopmost()
            elif str(key) == self.take_screenshot:
                self.pUpdateMap()
            elif str(key) == self.cycle_map:
                self.pCycleMap()
                
    def on_release(self, key):
        try:
            if key.char == self.toggle_overlay.replace("Key.", ""):
                self.removeTopmost()
        except:
            if str(key) == self.toggle_overlay:
                self.removeTopmost()
    
    def listen(self, *args):
        self.listener = Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        self.master.overrideredirect(True)
        #keyboard.on_press_key(self.toggle_overlay, self.makeTopmost, suppress=False)
        #keyboard.on_release_key(self.toggle_overlay, self.removeTopmost, suppress=False)
        #keyboard.on_press_key(self.take_screenshot, self.pUpdateMap, suppress=False)
        #keyboard.on_press_key(self.cycle_map, self.pCycleMap, suppress=False)
    def closeListen(self, *args):
        self.listener.stop()     
    
    def close_window(self, *args):
        self.master.destroy()

