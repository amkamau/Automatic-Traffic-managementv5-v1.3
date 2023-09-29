import os
import pandas as pd
import numpy as np

csvfilepath = "files/cache/postcache.csv"


def pandas_csv_create():
    # dictionary of lists
    dict = {
            'id': [int(1111),int(1112)], 
            'object': ["person","car"], 
            'color': [(140,140,140),(255,0,0)] , 
            'vx':[int(5),int(20)],
            'vy':[int(6),int(16)]
            }
    df = pd.DataFrame(dict)
    df.to_csv(csvfilepath, index=False,header=True)

def pandas_write(csvdata):
    csvdata = pd.DataFrame(csvdata)
    csvdata.to_csv(csvfilepath, index=False,header=True)

def pandas_csv_read():
    if not os.path.exists(csvfilepath):
        pandas_csv_create()
    data_import = pd.read_csv(csvfilepath)    
    return data_import

def get_vector(csvdata, obname,color,center,threshold=4):  
     
    names = csvdata["object"].to_numpy()
    vx = csvdata["vx"].to_numpy()
    vy = csvdata["vy"].to_numpy()
    
    dvx = np.where(np.absolute(np.subtract(vx,int(center[0]))) >= threshold, 0, 1)
    dvy = np.where(np.absolute(np.subtract(vy,int(center[1]))) >= threshold, 0, 1)  
    
    name_bitwise = np.where(names == obname, 1,0)
    dxdy_bitwise = np.bitwise_and(dvx,dvy)
    
    indexes = np.bitwise_and(name_bitwise,dxdy_bitwise)
    index = np.where(indexes == 1)[0]   
     
    obj_id = diffx = diffy = None
    
    if len(index) > 0:
        index = index[0]
        diffx = center[0] - int(csvdata["vx"][index])
        diffy = center[1] - int(csvdata["vy"][index])        
        obj_id = csvdata["id"][index]
        csvupdate = pd.DataFrame({"vector":[center]}, index=[index])
        csvdata.update(csvupdate)
                   
    else:
        obj_id = int(np.max(csvdata["id"]) + 1)
        data = pd.DataFrame({
                            'id': [int(obj_id)], 
                            'object':[obname], 
                            'color':[(color[0],color[1],color[2])], 
                            'vx':[int(center[0])],
                            'vy':[int(center[1])]
                            })
        csvdata = pd.concat([csvdata,data],ignore_index=True)
        diffx = 0
        diffy = 0
        
    return obj_id , (diffx,diffy), csvdata