from tkinter import *

def my_upd(overlay, sc1, sc2, sc3):
    color_c='#%02x%02x%02x' % (sc1.get(), sc2.get(), sc3.get())
    overlay.config(bg=color_c)   

