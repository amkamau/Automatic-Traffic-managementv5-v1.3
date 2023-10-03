import cv2
import numpy as np
import time
import os
from PIL import Image
import object_detect as objectdetect
import object_config as objectconfig
import object_json as objectjson
from threading import Thread

starting_time = time.time()
frame_id = 0
thresh = 5
frames_back = 3

object_color = (86, 0, 0)

trackfile = "files/tracking.txt"
configfile = "files/config.cfg"
objectconfig.initConfig()

trackfile_mod_time = 0
configfile_mod_time = 0
center_axis = False

class_list = objectdetect.loadClasses()


def trackObjects():
    with open(trackfile,"r") as tfile:
        data = tfile.read()
        return data.split("\n")
    

def annotateFrame(frame,fps,objects_detected,track_objects_total):        
    cv2.rectangle(frame, (0, 0), (300, 30), (10,10,10), -1)
    cv2.putText(frame, str("FPS : " + str(round(fps, 2))), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255,250,250))
    cv2.putText(frame, "Press (Q) to exit", (120, 20), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200))
    cv2.rectangle(frame, (0, 40), (200, 70), (10,10,10), -1)
    cv2.putText(frame, "Tracking: "+str(track_objects_total)+ " of " + str(objects_detected), (10, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255,250,250))    
    return frame


def dominantColor(frame):
    try:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
        image = Image.fromarray(frame)
        img = image.copy()
        img = img.convert("RGBA")
        img = img.resize((1, 1), resample=0)
        dominantColor = img.getpixel((0, 0))        
    except:
        dominantColor = (0,0,255)
    return dominantColor


def multiprocessFrame(frame, classid, confidence, box):  
    x1, x2, y1, y2 = box[0], (box[0] + box[2]), box[1], (box[1] + box[3])
    cx, cy = int(x1+x2)//2, int(y1+y2)//2      
    object_name = class_list[classid]    
    object_id = 0
    for x in range(frames_back):
        for i in jsondata[str(x)]:
            if i["object"] == object_name:
                fx1,fy1,fx2,fy2 = i["box"]
                f_width = int(abs(fx2-fx1))
                if abs(f_width - int(x2-x1)) <= thresh:
                    f_height = int(abs(fy2-fy1))
                    if abs(f_height - int(y2-y1))<= thresh:
                        object_id = i["id"]
                        break
                # dcx = int(abs(i["center"][0]-cx))
                # if dcx <= thresh:
                #     dcy = int(abs(i["center"][1]-cy))
                #     if dcy <= thresh:
                #         diff.append([int(i["id"]),dcx,dcy])
        if object_id != 0:
            break   
            
    object_text = str(object_name) +" "+ str(round(confidence,1)) +" : " +str(object_id)
    # np.append(object_list,{'id': int(object_id) , 'object': str(object_name), 'box': [int(x1),int(y1),int(x2),int(y2)], 'center': [int(cx),int(cy)], 'frame': np.array(frame[y1:y2,x1:x2]).tolist() })
    # cv2.imwrite('output.png', )
    grayscale = cv2.cvtColor(frame[y1:y2,x1:x2], cv2.COLOR_BGR2GRAY)
    object_list.append({'id': int(object_id) , 'object': str(object_name), 'box': [int(x1),int(y1),int(x2),int(y2)], 'center': [int(cx),int(cy)], 'frame': np.array(grayscale).tolist() })
    
    if configs['center_to_axis'] == "True":
        cv2.line(frame, (cx, cy),(int(fwidth/2), int(fheight/2)),object_color, thickness=1) 
    if configs['box_border'] == "True":
        cv2.rectangle(frame, box, (object_color), 2)
        cv2.rectangle(frame, (x1,y1-20),(x1+len(object_text)*6,y1), object_color, -1)
        cv2.putText(frame, object_text , (x1+3, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,255,255))
    cv2.circle(frame,center=(cx,cy),radius=2,color=(10,10,255),thickness=-1)   

def processFrame(frame,net):
    global fps, frame_id , track_objects, track_objects, configs, trackfile_mod_time, configfile_mod_time, object_list, jsondata, fwidth, fheight
   
    object_list = []
    fheight, fwidth , _ = frame.shape
    jsondata = objectjson.json_read()

    if trackfile_mod_time == 0 or trackfile_mod_time != os.stat(trackfile).st_mtime:
        trackfile_mod_time = os.stat(trackfile).st_mtime
        track_objects = trackObjects()
    if configfile_mod_time == 0 or configfile_mod_time != os.stat(configfile).st_mtime:
        configfile_mod_time = os.stat(configfile).st_mtime
        configs = objectconfig.readConfig()

    class_ids, confidences, boxes = objectdetect.getObjects(frame,net)
    
    frame_id+=1     
    object_count = 0
    threads = []
    for (classid, confidence, box) in zip(class_ids, confidences, boxes):
        if object_count >= int(configs["limit_track_count"]) and configs["limit_track"] == "True":
            break
        if class_list[classid] in track_objects:
            threads.append(Thread(target=multiprocessFrame,args=(frame, classid, confidence, box))) 
            object_count+=1               
    track_objects_total = len(threads)
    for thread in threads: thread.start()
    for thread in threads: thread.join()     

    objectjson.json_update(jsondata,object_list)

    fps = frame_id / (time.time() - starting_time)    
    frame = annotateFrame(frame,fps,len(class_ids),track_objects_total)

    return frame