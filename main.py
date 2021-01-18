##By Ph3nX-Z on github : https://github.com/Ph3nX-Z/  ##
import sqlite3
import sys
import os
from Crypto.Cipher import AES
import base64
import struct
import glob
from fernet_custom import *
from hash_lib import Hash
from tkinter.messagebox import *
from tkinter import *
from tkinter import simpledialog
from Suggest_lib import Suggested_pass
import subprocess
import pyperclip
from multithread import *
import requests

password_temp=""

logo="""
 _____  _____ _       _____                       _       ______                                   _ 
/  ___||  _  | |     /  __ \                     | |      | ___ \                                 | |
\ `--. | | | | |     | /  \/ ___  _ __  ___  ___ | | ___  | |_/ /_ _ ___ _____      _____  _ __ __| |
 `--. \| | | | |     | |    / _ \| '_ \/ __|/ _ \| |/ _ \ |  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` |
/\__/ /\ \/' / |____ | \__/\ (_) | | | \__ \ (_) | |  __/ | | | (_| \__ \__ \\ V  V / (_) | | | (_| |
\____/  \_/\_\_____/  \____/\___/|_| |_|___/\___/|_|\___| \_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
                                                                                                     
                                                                                                     
 _   __ _____ ___________ ___________                                                                
| | / /|  ___|  ___| ___ \  ___| ___ \                                                               
| |/ / | |__ | |__ | |_/ / |__ | |_/ /                                                               
|    \ |  __||  __||  __/|  __||    /                                                                
| |\  \| |___| |___| |   | |___| |\ \                                                                
\_| \_/\____/\____/\_|   \____/\_| \_|           \n\n"""                                                    
                                                                                                     
                                                                                                     
def refresh():
    if 'gestionnaire.db' in glob.glob("*.db"):
            conn = sqlite3.connect('gestionnaire.db')
    else:
        print('Connecting To Encrypted Database')
        conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd=f"SELECT * FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    for loop in range(2):
        for elem_remove in retour:
            listNodes.delete("0")
    for elem in retour:
        liste_mots=[]
        for element in elem:
            liste_mots.append(element)
        try:
            if liste_mots[0]!='0' and liste_mots[1]!='0' and liste_mots[2]!='Values_Init':
                text=f"  User: {liste_mots[0]}   Password: {liste_mots[1]}   site : {liste_mots[2]} "
                listNodes.insert(END,text)
                listNodes.insert(END,"")
        except:
            pass
print(logo)
def flush():
    password_flush=simpledialog.askstring("Validate","Please Enter Your Password :")
    hash2=Hash(password_flush)
    allow2=hash2.verify()
    if allow2==True:
        try:
            os.remove('gestionnaire.db')
        except:
            print("files dont exist")
        try:
            os.remove('gestionnaire_encrypted.db')
        except:
            print("files dont exist")
        try:
            os.remove('accounthash.hash')
        except:
            print("files dont exist")
        stop_server()
        with open("log.log",'a') as logfile:
            logfile.write("\n")
        sys.exit()
    else:
        messagebox.showwarning("Warning","Incorrect Password")
def create():
    if not 'gestionnaire.db' in glob.glob('*.db'):
        conn = sqlite3.connect('gestionnaire.db')
        conn.close()
    if not 'log.log' in glob.glob('*.log'):
        with open('log.log',"w") as file:
            file.write("")
    print('Creating or Changing password ...')
        


def stop_server():
    try:
        requests.get('http://127.0.0.1/StopServer')
    except:
        print("error")

def encrypt(passwd):

    conn = sqlite3.connect('gestionnaire.db')
    conn2 = sqlite3.connect('gestionnaire_encrypted.db')

    cur2=conn2.cursor()
    cur = conn.cursor()

    cmd2='CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);'
    cmd="SELECT * FROM gestionnaire;"

    cur2.execute(cmd2)
    cur.execute(cmd)

    conn2.commit()
    conn.commit()

    retour = cur.fetchall()

    for elements in retour:
        liste_encrypt=[]
        #print(elements)
        for element in elements:
            #print(element)
            element_encrypted=password_encrypt(element.encode(),passwd) #from fernet custom
            #print(element_encrypted)
            liste_encrypt.append(element_encrypted.decode("utf-8"))
        #print(liste_encrypt)
        
        try:
            cmd2=f"INSERT INTO gestionnaire(user, password, site) VALUES ('{liste_encrypt[0]}','{liste_encrypt[1]}','{liste_encrypt[2]}');"
            cur2.execute(cmd2)
            conn2.commit()
        except:
            print('Out of range: In Insertion')

        retour2 = cur2.fetchall()
        #print(retour2)

    cur2.close()
    conn2.close()
    cur.close()
    conn.close()
    os.remove('gestionnaire.db')
    with open('log.log','a') as filename:
        filename.write('Encrypted\n')
def decrypt(passwd):

    conn = sqlite3.connect('gestionnaire_encrypted.db')
    conn2 = sqlite3.connect('gestionnaire.db')

    cur2=conn2.cursor()
    cur = conn.cursor()

    cmd2='CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);'
    cmd="SELECT * FROM gestionnaire;"

    cur2.execute(cmd2)
    cur.execute(cmd)

    conn2.commit()
    conn.commit()

    retour = cur.fetchall()

    for elements in retour:
        liste_decrypt=[]
        #print(elements)
        for element in elements:
            #print(element)
            element_decrypted=password_decrypt(element.encode(),passwd) #from fernet custom
            #print(element_encrypted)
            liste_decrypt.append(element_decrypted.decode("utf-8"))
        #print(liste_decrypt)
        
        try:
            cmd2=f"INSERT INTO gestionnaire(user, password, site) VALUES ('{liste_decrypt[0]}','{liste_decrypt[1]}','{liste_decrypt[2]}');"
            cur2.execute(cmd2)
            conn2.commit()
        except:
            print('Out of range: In Insertion')
            with open('log.log','a') as logfile:
                logfile.write('[_] SQL Does not accept Bytes types objects')

        retour2 = cur2.fetchall()
        #print(retour2)

    cur2.close()
    conn2.close()
    cur.close()
    conn.close()
    os.remove('gestionnaire_encrypted.db')
    with open('log.log','a') as filename:
        filename.write('Decrypted\n')


def log(status):
    test = True
    if status == 'in':
        if "gestionnaire_encrypted.db" in glob.glob('*.db'):
            allow = False
            with open("log.log","a") as logfile:
                logfile.write('[+] Starting Database \n')
                if allow == False:
                    database_pass=password_login.get()
                    hash1 = Hash(database_pass)
                    allow = hash1.verify()
                    if allow == False:
                        messagebox.showwarning("Warning","Incorrect Password")
                        logfile.write(f"[_] Connexion Attempt with Password Hash :{Hash(database_pass)} \n")
                    else:
                        print("Login Successfully")
                        with open('var.txt','w') as varfile:
                            varfile.write('in')
                        try:
                            decrypt(database_pass)
                        except:
                            logfile.write('[_] Error in Decryption')
                global password_temp
                password_temp = database_pass

    elif status == 'out':
        with open('log.log','a') as logfile:
            logfile.write("[*] Shuting Down Database\n")
            if "gestionnaire.db" in glob.glob('*.db'):
                try:
                    encrypt(password_temp)
                except:
                    logfile.write('[-] Error in encryption')
                with open('var.txt','w') as varfile:
                    varfile.write('out')
                stop_server()
                with open("log.log",'a') as logfile:
                    logfile.write("\n")
                sys.exit()

def verif():
    if 'gestionnaire.db' in glob.glob("*.db"):
        conn = sqlite3.connect('gestionnaire.db')
    else:
        print('Connecting To Encrypted Database')
        conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd=f"SELECT * FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    for elem in retour:
        liste_mots=[]
        for element in elem:
            liste_mots.append(element)
        try:
            if liste_mots[0]!='0' and liste_mots[1]!='0' and liste_mots[2]!='Values_Init':
                print(f"User: {liste_mots[0]} Password: {liste_mots[1]} site : {liste_mots[2]}")
        except:
            pass
def verif_encrypt():
    conn = sqlite3.connect('gestionnaire_encrypted.db')
    cur = conn.cursor()
    cmd="SELECT* FROM gestionnaire;"
    cur.execute(cmd)
    conn.commit()

    retour = cur.fetchall()
    cur.close()
    conn.close()

def gestionnaire():
    conn = sqlite3.connect('gestionnaire.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS gestionnaire(user TEXT, password TEXT, site TEXT);")
    cur.execute("INSERT INTO gestionnaire(user, password, site) VALUES ('0','0','Values_Init');")
    conn.commit()

    retour = cur.fetchall()
    #print(retour)

    cur.close()
    conn.close()

def add_mdp():

    conn = sqlite3.connect('gestionnaire.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM gestionnaire")
    conn.commit()
    retour_ajust = cur.fetchall()
    cur.close()
    conn.close()
    refresh()

    if password_temp=="":
        messagebox.showwarning("Warning","Please Login")
    elif len(retour_ajust)==30:
        messagebox.showwarning("Warning","Please Open A New Db, limit excedeed")
    else:
        user=useradd.get()
        if check_var_pass.get()==1:
            pass1=Suggested_pass(5,5,5)
            password=pass1.generate()
        else:
            password=userpass.get()
        site=usersite.get()
        data=(user,password,site)
        conn = sqlite3.connect('gestionnaire.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO gestionnaire(user, password, site) VALUES (?,?,?);",data)
        conn.commit()

        retour = cur.fetchall()
        #print(retour)
        cur.close()
        conn.close()



with open('var.txt','w') as varfile:
        varfile.write('out')


def verify_server():
    try:
        requests.head("http://127.0.0.1/")
        server="UP"
    except:
        server="DOWN"


    text="Server: "+str(server)
    l5=LabelFrame(root,text="SERVER")
    l5.pack()
    serverbutton=Button(l5,text='Start Server', command=start_server).pack(side=LEFT)
    #serverbutton2=Button(l5,text='Stop Server',command=stop_server).pack(side=LEFT)
    textbox_server=Label(l5,text=text).pack(side=LEFT)
    l5.place(relx=0, relheight=0.12, relwidth=0.5,rely=0.55)
    root.after(10000,verify_server)


def verify():
    with open('var.txt','r') as varfile:
        data=varfile.read()
        if data=="in":
            loginstatus='Logged'
        else:
            loginstatus='Not Logged'


    text="Status: "+str(loginstatus)
    l6=LabelFrame(root,text="LOGIN STATUS")
    l6.pack()
    textbox3=Label(l6,text=text).pack(side="left")
    l6.place(relx=0.5, relheight=0.12, relwidth=0.5,rely=0.55)
    
    root.after(3000,verify)

def choix(choix):
    #choix=int(input(f"[--] - 1.Flush 2.Create/Change Pass (if logged) 3.Login 4.Add 5.Content 6.Logout   :"))
    if choix==1:
        flush()
    elif choix==2:
        password_user=password_create.get()
        if 'gestionnaire_encrypted.db' in glob.glob("*.db"):
            with open('var.txt','w') as varfile:
                varfile.write('out')
            messagebox.showwarning("Warning","Please Login")
            sys.exit()
        create()
        gestionnaire()
        

        hash_user=Hash(password_user)
        with open('accounthash.hash','w') as hashwrite:
            hash_user.hasher()
            hashwrite.write(hash_user.hash)

        encrypt(password_user)
        sys.exit()
    elif choix==3:
        log('in')
        refresh()
    elif choix==4:
        add_mdp()
        refresh()
    elif choix==5:
        verif()
    elif choix==6:
        log('out')

    #################################### DEV TOOLS
    elif choix==8:                     # DEV TOOLS
        encrypt('password')            # DEV TOOLS
    elif choix==9:                     # DEV TOOLS
        verif_encrypt()                # DEV TOOLS
    elif choix==10:                    # DEV TOOLS
        decrypt('password')            # DEV TOOLS
    #################################### DEV TOOLS
    print('\n')

def clipboard(mode):
    creds=listNodes.get(ACTIVE)
    splitted=creds.split(" ")
    if mode==1:
        tocopy=str(splitted[7])
    elif mode==2:
        tocopy=str(splitted[3])
    pyperclip.copy(tocopy)

def remove():
    creds=listNodes.get(ACTIVE)
    splitted=creds.split(" ")
    if password_temp!="":
        try:
            conn = sqlite3.connect('gestionnaire.db')
            cur = conn.cursor()
            cmd=f"DELETE FROM gestionnaire WHERE user='{splitted[3]}' AND password='{splitted[7]}' AND site='{splitted[12]}';"
            cur.execute(cmd)
            conn.commit()

            retour = cur.fetchall()
        #print(retour)

            cur.close()
            conn.close()
        except:
            print("error sql")
    else:
        messagebox.showwarning("Warning","Please Login")
    refresh()
def start_server():
    start_server_multi(password_temp)
    

root = Tk()
root.title("PasswordKeeper")
root.geometry("700x650")
password_create=StringVar()
check_var_pass=IntVar()
password_login=StringVar()
useradd=StringVar()
userpass=StringVar()
usersite=StringVar()

l=LabelFrame(root, text="LOG OPTIONS")
l.pack(side=RIGHT)

l2=LabelFrame(root,text='ACTIONS')
l2.pack(side=LEFT)

l3=LabelFrame(root,text="CONTENT")
l3.pack()

l4=LabelFrame(root,text="ADD")
l4.pack(padx=50)

l5=LabelFrame(root,text="SERVER")
l5.pack()

l6=LabelFrame(root,text="LOGIN STATUS")
l6.pack()

flushing = Button(l2, text='Remove current DB',command=lambda: choix(1)).pack()


text=Label(l2,text="New Password :").pack()
password_creation= Entry(l2, textvariable=password_create).pack() 
creation = Button(l2, text='Change Password',command=lambda: choix(2)).pack()
text_warranty_= Label(l2,text="\n").pack(side=BOTTOM)
text_warranty__= Label(l2,text="##############################################################\n").pack(side=BOTTOM)
text_warranty= Label(l2,text="Security Info: Password Stored and Encrypted With Safe Methods").pack(side=BOTTOM)
text_warranty_= Label(l2,text="\n##############################################################").pack(side=BOTTOM)
#check=Checkbutton(l2, text="Destroy previous", variable=check_var).pack()

text2=Label(l,text="Database Password (q to quit):").pack()
password_entry = Entry(l, textvariable=password_login).pack() 
submit = Button(l, text='Connect',command=lambda: choix(3)).pack(side=LEFT)
submit2 = Button(l, text='Disconnect',command=lambda:choix(6)).pack(side=RIGHT)

text3=Label(l4,text="User :").pack(side=TOP, anchor=NW)
User_Entry = Entry(l4, textvariable=useradd).pack(side=TOP, anchor=NE, fill=X) 
text3=Label(l4,text="Password :").pack(side=TOP, anchor=NW)
Password_User_Entry = Entry(l4, textvariable=userpass).pack(side=TOP, anchor=NE, fill=X)
text4=Label(l4,text="Site :").pack(side=TOP, anchor=NW)
site_user_entry = Entry(l4, textvariable=usersite).pack(side=TOP, anchor=NE, fill=X)
submit21 = Button(l4, text='Add',command=lambda: choix(4),borderwidth=0.5).pack(side=LEFT)
check=Checkbutton(l4, text="Random Pass", variable=check_var_pass).pack(side=RIGHT,padx=20)

serverbutton=Button(l5,text='Start Server', command=start_server).pack(side=LEFT)
#serverbutton2=Button(l5,text='Stop Server',command=stop_server).pack(side=LEFT)

listNodes=Listbox(l3, width=90, heigh=10)
listNodes.pack(side=RIGHT)

scrollbar=Scrollbar(l3, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill='y')

listNodes.config(yscrollcommand=scrollbar.set)

refresh_button=Button(l3,text="Refresh",command=refresh).pack()
remove_button=Button(l3,text="Remove", command=remove).pack()
copy_button=Button(l3,text="Copy Password",command=lambda:clipboard(1)).pack()
copy_user=Button(l3,text="Copy User",command=lambda: clipboard(2)).pack()


l.place(relx=0, relheight=0.25, relwidth=0.5)
l2.place(relx=0.5, relheight=0.55, relwidth=1.0 - 0.5)
l3.place(relheight=0.3, relwidth=1.0,rely=0.68)
l4.place(relx=0, relheight=0.30, relwidth=0.5,rely=0.25)
l5.place(relx=0, relheight=0.12, relwidth=0.5,rely=0.55)
l6.place(relx=0.5, relheight=0.12, relwidth=0.5,rely=0.55)
root.after(5000,verify)
root.after(2000,refresh)
root.after(30000,verify_server)
root.mainloop()
if 'gestionnaire.db' in glob.glob("*.db"):
    encrypt(password_temp)

stop_server()
os.remove('./backup/backup.db')
with open("log.log",'a') as logfile:
    logfile.write("\n")