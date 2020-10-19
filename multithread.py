import threading
import time
from flask import Flask
import os
import signal


global app
app=Flask(__name__)
#############################################
@app.route('/')                             #
def hello():                                # 
    return "Hello word"                     # A CHANGER POUR METTRE SITE
                                            #
                                            #
#############################################
@app.route('/StopServer', methods=['GET'])
def StopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return "server down"

class myThread (threading.Thread):
    def __init__(self, threadID, name, status):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.status = status
    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        app.run(port=9999)
        threadLock.release()
def start_server_multi():
    global threadLock
    threadLock = threading.Lock()
    threads = []

    # Create new threads
    thread1 = myThread(1, "Thread-1", 1)


    # Start new Threads
    p=thread1.start()

    # Add threads to thread list
    threads.append(thread1)