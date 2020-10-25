import sqlite3
import glob
import os
from tkinter.messagebox import *
from tkinter import *
import time
import subprocess
from fernet_custom import *
from hash_lib import Hash


def refresh():
    for elem in glob.glob("*.db"):
        listNodes.delete("0")
    for elem in glob.glob("*.db"):
        listNodes.insert(END,elem)
def rename(number,liste):
    with open('name.txt','r') as namefile:
        name=namefile.read()
        name=name.split('\n')[0]
    for element in liste:
        if str(number) in element:
            element2=element.split(". ")
            element2=element2[1]
        os.rename(element2,name)#################ici
        break

def rename2(number,liste):
    for element in liste:
        if str(number) in element:
            element2=element.split(" ")
            element2=element2[1]
            os.rename(element2,'gestionnaire_encrypted.db')
    with open('name.txt','w') as namefile:
        namefile.write(element2)#######ici
    print(element2)
    element2=element2[0:-3]
    os.rename(element2+'.hash','accounthash.hash')
    with open('hashname.txt','w') as hashfile:
        hashfile.write(element2)
    with open("log.log",'a') as logfile:
        logfile.write(f'{element2} selected \n')
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

def display():
    compteur=0
    liste=[]
    for files in glob.glob('*.db'):
        compteur+=1
        elem=f'{str(compteur)}. {files}'
        liste.append(elem)
    return liste

def select():
    db=listNodes.get(ACTIVE)
    print("db :",db)
    if db!="":
        liste=display()
        for i in liste:
            mot_split=i.split(' ')
            numero=mot_split[0].split('.')
            if mot_split[1]==db:
                rename2(int(numero[0]),liste)
                break
        root.destroy()
    else:
        messagebox.showwarning("Warning","Select a Database")

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
    password_temp=password_field.get()
    encrypt(password_temp)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        sys.exit()

def create():
    if not 'gestionnaire.db' in glob.glob('*.db'):
        conn = sqlite3.connect('gestionnaire.db')
        conn.close()
    if not 'log.log' in glob.glob('*.log'):
        with open('log.log',"w") as file:
            file.write("")
    print('Creating or Changing password ...')
    gestionnaire()
    name=user_field.get()
    password_user=password_field.get()
    os.rename('gestionnaire_encrypted.db',str(name)+'.db')
    hash_user=Hash(password_user)
    with open('accounthash.hash','w') as hashwrite:
        hash_user.hasher()
        hashwrite.write(hash_user.hash)
    os.rename('accounthash.hash',str(name)+'.hash')
    refresh()
split=0.5
root = Tk()
root.title("Launcher")
root.geometry("600x330")
password_field=StringVar()
user_field=StringVar()

label_big = Label(root, text="Launcher", font=("Times New Roman", 35, "bold")).pack()

l=LabelFrame(root, text="ACTIONS")
l.pack(side=RIGHT)

l2=LabelFrame(root, text="CONTENT")
l2.pack(side=LEFT)

listNodes=Listbox(l2, width=35, heigh=10)
listNodes.pack()
scrollbar=Scrollbar(l2, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill='y')
listNodes.config(yscrollcommand=scrollbar.set)

submit = Button(l, text='Select',command=select).pack()
submit2 = Button(l, text='Refresh',command=refresh).pack()
text=Label(l,text="Password :").pack()
password_ENTRY= Entry(l, textvariable=password_field).pack() 
text1=Label(l,text="Name :").pack()
User_ENTRY= Entry(l, textvariable=user_field).pack() 
submit3 = Button(l, text='Create',command=create).pack()

l.place(relx=0, relheight=1, relwidth=split, rely=0.2)
l2.place(relx=split, relheight=1, relwidth=1.0 - split, rely=0.2)

root.after(500,refresh)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
subprocess.call("python main.py", shell=False)

with open('name.txt','r') as file_name:
    data=file_name.read().split("\n")
    data=data[0]
for i in glob.glob("*.db"):
    if i=='gestionnaire_encrypted.db':
        os.rename(i,data)
if 'accounthash.hash' in glob.glob("*.hash"):
    with open("hashname.txt",'r') as hashfile:
        rename_hash=hashfile.read()
    os.rename('accounthash.hash',rename_hash+'.hash')

'''
if 'gestionnaire.db' in glob.glob("*.db"):
    encrypt(password_temp)'''