from tkinter import *
import object_config as objectconfig
import gui_configframe as configframe
import gui_listbox as listbox
import gui_finetrack as finetrack

root = Tk()
root.title("Smart Traffic")
root.iconphoto(False, PhotoImage(file = 'images/icon2.png') )
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("700x900+"+str(screen_width-750)+"+50")

font_normal = 'Helvetica 10 normal'
font_bold = 'Helvetica 11 bold'
myrelief = "solid"

#########################################################################################################
#### Frame 0
listbox.frame_one(root)

#########################################################################################################
#### Frame 1 - Configurations
list_label = Label(root,text="Configurations",font=font_bold).place(x=330,y=10)
frame1 = Frame(root, relief=myrelief,border=1,width=350,height=200)
frame1.place(x=330,y=35)
configframe.frame_one(frame1)


#########################################################################################################
#### Frame 2 - Fine grained tracking
list_label = Label(root,text="Fine Grained Tracking",font=font_bold).place(x=330,y=270)
frame2 = Frame(root, width=350,height=300,relief=myrelief,border=1)
frame2.place(x=330,y=300)
finetrack.frame_one(frame2)


#########################################################################################################
#### Frame 3 - Quick Actions
list_label = Label(root,text="Quick Action",font=font_bold).place(x=330,y=650)
frame3 = Frame(root, width=350,height=210,relief=myrelief,border=1)
frame3.place(x=330,y=680)
button_trackall = Button(frame3,text="Track All",padx=10,pady=5,font=font_normal,bg="#002147",fg="#ffffff",relief="raised",command=lambda: listbox.trackAll(True))
button_trackall.place(x=10,y=20)
button_trackall = Button(frame3,text="Clear Tracking List",padx=10,pady=5,font=font_normal,bg="#0F0F0F",fg="#ffffff",relief="raised",command=lambda: listbox.trackAll(False))
button_trackall.place(x=10,y=70)
   


root.mainloop()