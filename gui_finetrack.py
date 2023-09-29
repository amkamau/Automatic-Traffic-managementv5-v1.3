from tkinter import *
import object_config as objectconfig

configs = objectconfig.readConfig()        
box_border = True if configs["box_border"] == "True" else False

def frame_one(frame):
    finebutton_var = BooleanVar()
    finebutton_var.set(box_border)
    fine_button = Checkbutton(frame, text = "Enabled", variable=finebutton_var,onvalue=True,offvalue=False,command=lambda: objectconfig.updateConfig("fine_tracking",finebutton_var.get()))
    fine_button.place(x=5,y=5)
