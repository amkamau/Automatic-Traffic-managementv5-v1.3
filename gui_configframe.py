from tkinter import *
import object_config as objectconfig


## Default configs from file
configs = objectconfig.readConfig()        
center_to_axis = True if configs['center_to_axis'] == "True" else False
limit_track = True if configs['limit_track'] =="True" else False
limit_track_count = int(configs['limit_track_count'])
fine_tracking = True if configs['fine_tracking'] == "True" else False
box_border = True if configs["box_border"] == "True" else False

def applyLimit():    
    if limittrack_var.get():
        objectconfig.updateConfig("limit_track_count",limittrack_spinner.get())
        limittrackbutton_alert.config(text="Applied ("+str(limittrack_spinner.get())+")",fg="#22aa22")
    else:
        limittrackbutton_alert.config(text="Enable this option first ",fg="#aa2222")

def frame_one(frame):
    global limittrack_var, limittrack_spinner, limittrackbutton_alert
    
    ### 
    # 1 checkbutton
    centertoaxis_var = BooleanVar()
    centertoaxis_var.set(center_to_axis)
    centertoaxis_button = Checkbutton(frame, text = "Draw line from object to center of the frame", variable=centertoaxis_var,onvalue=True,offvalue=False,command=lambda: objectconfig.updateConfig("center_to_axis",centertoaxis_var.get())) 
    centertoaxis_button.place(x=5,y=10)
    # 2 checkbutton
    limittrack_var = BooleanVar()
    limittrack_var.set(limit_track)
    limittrack_button = Checkbutton(frame, text = "Limit number of objects tracked", variable=limittrack_var,onvalue=True,offvalue=False,command=lambda: objectconfig.updateConfig("limit_track",limittrack_var.get()))
    limittrack_button.place(x=5,y=40)    
    # 3 spinbox
    limittrackspinner_var = IntVar()
    limittrackspinner_var.set(int(limit_track_count))
    limittrack_spinner = Spinbox(frame, from_= 1, to = 20, width=10, textvariable=limittrackspinner_var)
    limittrack_spinner.place(x=40,y=70)    
    # 4 button
    limittrackcount_button = Button(frame,text="Apply",command=applyLimit)
    limittrackcount_button.place(x=120,y=70)
    # 5 label
    limittrackbutton_alert = Label(frame,text="")
    limittrackbutton_alert.place(x=180,y=70)
    # 6 checkbutton
    boxborder_var = BooleanVar()
    boxborder_var.set(box_border)
    boxborder_button = Checkbutton(frame, text = "Image Border line", variable=boxborder_var,onvalue=True,offvalue=False,command=lambda: objectconfig.updateConfig("box_border",boxborder_var.get()))
    boxborder_button.place(x=5,y=100)
    # 7
