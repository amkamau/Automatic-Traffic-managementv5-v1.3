# Python program to convert JSON to Python
import json
import os

jsonfile = "files/db.json"
frame_count = 10

def get_id(list):
    ids = []
    for i in list:
        ids.append(int(i["id"]))
    return int(sorted(ids)[-1]) + 1

def json_init():
    if not os.path.exists(jsonfile) or os.stat(jsonfile).st_size == 0:
        dict = {}
        for i in range(frame_count):
            x1,y1,x2,y2 = 1,1,2,2
            dict[str(i)] = [ { 'id': int(i+1), 'object': "person", 'box' : [x1,y1,x2,y2], 'center': [1,1], 'frame' : []} ]
        with open(jsonfile, "w") as f:
            f.write(json.dumps(dict, indent = 4, sort_keys= False) )  

def json_read():
    json_init()
    with open(jsonfile, 'r') as f:
        jdata = json.load(f)
    return jdata

def json_write(dict):
    json_init()
    with open(jsonfile, "w") as file:
            json.dump(dict, file, indent=4)

def json_update(dict,list):
    dict_new = {}
    last_id = 0
    for i in list:
        if i["id"] == 0:
            if last_id == 0:
                last_id = get_id(list) 
            i["id"] = last_id
            last_id+=1 
    for i in range(len(dict)):
        if i == 0:
            dict_new[str(i)] = list
        else:
            dict_new[str(i)] = dict[str(i-1)]
    json_write(dict_new) 
    
# print(len(json_read()))