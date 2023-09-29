import subprocess
from threading import Thread

def openMain(): 
    subprocess.run(["python", "main.py"])

def openGui():
    subprocess.run(["python", "gui.py"])


Thread(target = openMain).start() 
Thread(target = openGui).start()