import configparser
import os

configfile = "files/config.cfg"
config = configparser.ConfigParser()


def initConfig():
    if not os.path.exists(configfile):
        config['Section 1'] = {
                                "center_to_axis" : False,
                                "limit_track" : False,
                                "limit_track_count" : 1,
                                "fine_tracking" : False
                                }
        with open(configfile, 'w') as file:
            config.write(file)

def readConfig():
    initConfig()
    config.read(configfile)    
    details_dict = dict(config.items('Section 1'))
    return details_dict

def getKey(key):
    dict = readConfig()
    return dict[key]

def updateConfig(key,value):
    initConfig()
    dict = readConfig()
    if isinstance(key, list) and isinstance(value,list):
        if len(key) == len(value):
            for i in range(len(key)):
                dict[key[i]] = value[i]
    else:
        dict[key] = value   
    
    config['Section 1'] = dict
    with open(configfile, 'w') as file:
        config.write(file)


## Load all trackable objects from text file
def loadObjects():
    class_list = []
    with open("files/objects.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]
    return sorted(class_list)

## Load tracking items from tracking list
def loadTracking():
    class_list = []
    with open("files/tracking.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]
    return sorted(class_list)


## Update tracking file   
def writeTracking(list_tracking):
    sorted(list_tracking)
    with open("files/tracking.txt","w") as f:
        for line in list_tracking:
            f.write(f"{line}\n")