from tkinter import *
import object_config as objectconfig

font_normal = 'Helvetica 10 normal'
font_bold = 'Helvetica 11 bold'
myrelief = "solid"

## Sort listbox items        
def sortlistTracking():
    listbox_turple_nontracking = sorted(list_non_tracking.get(0,END))
    listbox_turple_tracking = sorted(list_tracking.get(0,END))
    list_non_tracking.delete(0,END)
    list_tracking.delete(0,END)
    [ list_non_tracking.insert(i, listbox_turple_nontracking[i]) for i in range(len(listbox_turple_nontracking)) ]
    [ list_tracking.insert(i, listbox_turple_tracking[i]) for i in range(len(listbox_turple_tracking)) ]
         
## Remove item from tracking list
def pasteto(event=1):
    try:
        n1 = list_tracking.curselection()[0] # index of the item selected
        i1 = list_tracking.get(n1) # the item string
        list_tracking.delete(n1)
        list_non_tracking.insert(END, i1)
        sortlistTracking()    
        objectconfig.writeTracking(list_tracking.get(0,END))
    except:pass

## Add item to tracking list
def pasteback(event=1):
    try:
        n1 = list_non_tracking.curselection()[0] # index of the item selected
        i1 = list_non_tracking.get(n1) # the item string
        list_non_tracking.delete(n1)
        list_tracking.insert(END, i1)
        sortlistTracking()
        objectconfig.writeTracking(list_tracking.get(0,END))
    except:pass

## add all items to tracking list
def trackAll(condition):
    all_items = sorted( objectconfig.loadObjects())
    list_non_tracking.delete(0,END)
    list_tracking.delete(0,END)
    if condition:
        [ list_tracking.insert(END, n) for n in all_items ]        
    else:    
        [ list_non_tracking.insert(END, n) for n in all_items]
    objectconfig.writeTracking(list_tracking.get(0,END))

def frame_one(root):
    global list_tracking, list_non_tracking
    ## Put items into list
    # list 1
    list_label = Label(root,text="Tracking",font=font_bold).place(x=10,y=10)
    list_tracking = Listbox(root,height=50,width=20,font=font_normal,border=1,relief=myrelief)
    list_tracking.place(x=15,y=35)
    list_tracking.bind("<Double-Button>", pasteto)
    # list 2
    list_label = Label(root,text="Not Tracking",font=font_bold).place(x=170,y=10)
    list_non_tracking = Listbox(root,height=50,width=20,font=font_normal,border=1,relief=myrelief)
    list_non_tracking.place(x=170,y=35)
    list_non_tracking.bind("<Double-Button>", pasteback)

    #class_lists = loadObjects()
    tracking = objectconfig.loadTracking()
    non_tracking = [i for i in  objectconfig.loadObjects() if i not in tracking]
    [ list_non_tracking.insert(END, n) for n in non_tracking]
    [ list_tracking.insert(END, n) for n in tracking ]