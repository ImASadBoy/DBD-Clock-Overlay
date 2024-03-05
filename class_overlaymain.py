import tkinter as tk
import customtkinter as ctk
from grab_screen import *
import configparser
from class_dbdoverlay import *
from upconfigs import *

con = configparser.ConfigParser()

def testfu(arg):
    print(arg)

class mainApp:
    def __init__(self):
        #get Screen Info
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()
        self.config = con.read("config/settings.ini")
        self.toggle_overlay = con["keybinds"]["toggle_overlay"]
        self.take_screenshot = con["keybinds"]["screenshot"]
        self.cycle_map = con["keybinds"]["cycle_map"]
        self.variation = con["gui"]["variation"]
        self.master = ctk.CTk()
        self.master.geometry("500x813")
        self.font = ('Onyx',28,'normal')
        
        #Alpha Slider
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid()
        self.tAlpha = ctk.CTkLabel(self.frame, text="Choose Overlay Transparency", font = self.font)
        self.tAlpha.grid(row=0,column=0,pady=10)
        self.sAlpha = ctk.CTkSlider(self.frame, from_=0, to=10, width = 500, height= 20, command=self.updateOvrl, progress_color= "#FFE0E3", button_color= "#ffb3ba", button_hover_color = "#ff99a3")
        self.sAlpha.grid(row=1,column=0,pady=10)
        self.sAlpha.set(float(con["DEFAULT"]["alpha"]))
        
        #Size Slider
        self.tSize = ctk.CTkLabel(self.frame, text="Overlay Scale", font = self.font)
        self.tSize.grid(row=2,column=0,pady=10)
        self.sSize = ctk.CTkSlider(self.frame, from_=0, to=300, number_of_steps= 30, width = 500, height= 20, command=self.updateOvrl, progress_color= "#FFE0E3", button_color= "#ffb3ba", button_hover_color = "#ff99a3")
        self.sSize.grid(row=3,column=0,pady=10)
        self.sSize.set(float(con["DEFAULT"]["addsize"]))
        
        #Movement Slider
        self.frame2 = ctk.CTkFrame(self.master)
        self.frame2.grid(pady =10)
        self.tX = ctk.CTkLabel(self.frame2, text="Move Overlay Position in the Screen", font = self.font)
        self.tX.grid(row=4,column=0,pady=15)
        self.sX = ctk.CTkSlider(self.frame2, from_=0, to=self.screen_width, width = 480, height= 20, command=self.updateOvrl, progress_color = "#FFE0E3", button_color= "#ffb3ba", button_hover_color = "#ff99a3")
        self.sX.grid(row=5,column=0,pady=3)
        self.sX.set(int(con["DEFAULT"]["positionx"]))
        self.sY = ctk.CTkSlider(self.frame2, from_=0, to=self.screen_height, width = 20, height= 300, orientation = "vertical", command=self.updateOvrl, progress_color= "#FFE0E3", button_color= "#ffb3ba", button_hover_color = "#ff99a3")
        self.sY.grid(row=5,column=1,pady=3)
        self.sY.set(self.screen_height - int(con["DEFAULT"]["positiony"]))
        
        #Keybinds
        self.frame3 = ctk.CTkFrame(self.master)
        self.frame3.grid(pady =5)
        self.tKey = ctk.CTkLabel(self.frame3, text="Change Keybinds", font = self.font, width= 360)
        self.tKey.grid(row=6,column=0,pady=15)
        self.tKey1 = ctk.CTkLabel(self.frame3, text= "Toggle Overlay", font = ('Onyx',16,'normal'), justify="right", anchor="e")
        self.tKey1.grid(row=7,column=0,pady=15)
        self.bKey1 = ctk.CTkButton(self.frame3, text= self.toggle_overlay.replace("Key.", "").upper(), command=lambda:self.updateKeys("toggle_overlay", self.bKey1),  font= ('Onyx',16,'normal'),fg_color= "#ffb3ba", hover_color= "#ff99a3")
        self.bKey1.grid(row=7, column = 1)
        self.tKey2 = ctk.CTkLabel(self.frame3, text="Take Screenshot", font = ('Onyx',16,'normal'), justify="right", anchor="e")
        self.tKey2.grid(row=8,column=0,pady=15)
        self.bKey2 = ctk.CTkButton(self.frame3, text=self.take_screenshot.replace("Key.", "").upper(), command=lambda:self.updateKeys("screenshot", self.bKey2), font= ('Onyx',16,'normal'),fg_color= "#ffb3ba", hover_color= "#ff99a3")
        self.bKey2.grid(row=8, column = 1)
        self.tKey3 = ctk.CTkLabel(self.frame3, text="Cycle Map Variation", font = ('Onyx',16,'normal'), justify="right", anchor="e")
        self.tKey3.grid(row=9,column=0,pady=15)
        self.bKey3 = ctk.CTkButton(self.frame3, text=self.cycle_map.replace("Key.", "").upper(), command=lambda:self.updateKeys("cycle_map", self.bKey3), font= ('Onyx',16,'normal'),fg_color= "#ffb3ba", hover_color= "#ff99a3")
        self.bKey3.grid(row=9, column = 1)
        self.openOverlay()
        #self.butnew("Click to open Window 2", dbdOverlay)
        self.master.resizable(False,False)
        ico = Image.open('assets/others/ico.ico')
        photo = ImageTk.PhotoImage(ico)
        self.master.wm_iconphoto(False, photo)
        self.master.title("DBD Clock Overlay")

    def templisten(self, key):
        print(key)
        updateKeybinds(self.to_change, key)
        #keyWindow(self.master, key)#, self.master.winfo_screenwidth(), self.master.winfo_screenheight(), self.master.winfo_x(), self.master.winfo_y())
        self.config= con.read("config/settings.ini")
        self.openOverlay()
        self.updateKeyBtn()
        return False

    def updateKeys(self, keybind, btn):
        self.new.closeListen()
        self.new.close_window()
        self.to_change = keybind
        btn.configure(text="PRESS A KEY", state = "disabled")
        templistener = Listener(on_release=self.templisten)
        templistener.start()
        
    
    def updateKeyBtn(self, *args):
        self.bKey1.configure(text=con["keybinds"]["toggle_overlay"].replace("Key.", "").upper(), state = "normal")
        self.bKey2.configure(text=con["keybinds"]["screenshot"].replace("Key.", "").upper(), state = "normal")
        self.bKey3.configure(text=con["keybinds"]["cycle_map"].replace("Key.", "").upper(), state = "normal")
        
    def updateOvrl(self, *args):
        self.ovrl.wm_deiconify()
         #alpha
        aValue = self.sAlpha.get()
        self.ovrl.attributes("-alpha", aValue/10)
        updateConfig("alpha", round(aValue))
        #scale
        addSize = int(round(self.sSize.get()))
        newSize = str(450 + addSize) + "x" + str(500 + addSize)
        xygeo = (newSize)
        self.ovrl.geometry(xygeo)
        updateConfig("addsize", str(addSize))
        self.new.resizeImg()
        #movement
        xValue = str(round(self.sX.get()))
        yValue = str(self.screen_height - round(self.sY.get()))
        xygeo = ("+" + xValue + "+" + yValue)
        self.ovrl.geometry(xygeo)
        updateConfig("positionx", xValue)
        updateConfig("positiony", yValue)
        self.ovrl.update_idletasks()
        
    def openOverlay(self):
        self.ovrl = ctk.CTkToplevel(self.master)
        self.new = dbdOverlay(self.ovrl)
        self.ovrl.overrideredirect(True)
        self.new.listen()
        
    def startApp(self, *args):
        self.master.mainloop()
    
    
    
app = mainApp()
app.startApp()
