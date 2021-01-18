import threading
import time
from flask import Flask
import os
import signal
from flask import Flask, session, request, render_template
import sqlite3

global app
app=Flask(__name__)
app.secret_key = os.urandom(24)
#############################################
@app.route('/', methods=['GET','POST'])                     
def index():
    conn = sqlite3.connect('gestionnaire.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM gestionnaire;")
    conn.commit()
    retour = cur.fetchall()
    cur.close()
    conn.close()
    retour.pop(0)
    retour_final = []
    for ligne in retour:
        ligne = str(ligne)
        ligne = ligne[1:-1]
        ligne_split = ligne.split(",")
        to_retour = "  :  ".join(ligne_split)
        to_retour = to_retour.replace("'"," ")
        retour_final.append(to_retour+'\n')
    #retour_final.insert(0,"")
    #retour_final.insert(0,"USER - PASSWORD - SITE")
    if request.method == 'GET':                              
        return render_template("index.html", db_output=retour_final)

                                           
@app.route('/StopServer', methods=['GET','POST'])
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
        app.run(port=80,threaded=True,host="0.0.0.0")
        threadLock.release()
def start_server_multi(password):
    global password_var
    password_var = password
    global threadLock
    threadLock = threading.Lock()
    threads = []

    # Create new threads
    thread1 = myThread(1, "Thread-1", 1)


    # Start new Threads
    p=thread1.start()

    # Add threads to thread list
    threads.append(thread1)