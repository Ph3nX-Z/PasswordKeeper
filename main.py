import sqlite3
import sys
import os
from Crypto.Cipher import AES
import base64
import struct
import glob
from fernet_custom import *
from hash_lib import Hash




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
                                                                                                     
                                                                                                     

print(logo)
def flush():
    try:
        os.remove("log.log")
    except:
        print("files dont exist")
    try:
        os.remove('gestionnaire.db.encrypted')
    except:
        print("files dont exist")
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
def create():
    if not 'gestionnaire.db' in glob.glob('*.db'):
        conn = sqlite3.connect('gestionnaire.db')
        conn.close()
    if not 'log.log' in glob.glob('*.log'):
        with open('log.log',"w") as file:
            file.write("")
    print('Creating or Changing password ...')
        



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
    test=True
    if status=='in':
        try:
            #if log_data_splitted[0]=="Encrypted":
            if "gestionnaire_encrypted.db" in glob.glob('*.db'):
                todo=False
            else:
                todo=True
        except:
            todo=True
        with open('log.log','a') as logfile:
            if todo==True:
                print("Please Create a database First")

            elif todo==False:
                allow=False
                logfile.write('[+] Starting Database \n')
                while allow==False:
                    database_pass=input("Database Password (press q to quit) :")
                    if database_pass=="q":
                        with open('var.txt','w') as varfile:
                            varfile.write('out')
                        sys.exit()
                    hash2=Hash(database_pass)
                    allow=hash2.verify()
                    if allow==False:
                        print("Wrong Password")
                        logfile.write(f"[_] Connexion Attempt with Password :{database_pass}")
                    else:
                        print("Login Successfully")
                        with open('var.txt','w') as varfile:
                            varfile.write('in')
                try:
                    decrypt(database_pass)
                except:
                    #print("error in decryption")
                    logfile.write('[_] Error in Decryption')


                global password_temp
                password_temp=database_pass

    elif status=='out':
        with open('log.log','a') as logfile:
            logfile.write("[*] Shuting Down Database\n")
            try:
                if password_temp==None:
                    password_temp=input("Type Your Password Please :")
            except:
                sys.exit()
            if "gestionnaire.db" in glob.glob('*.db'):
                try:
                    encrypt(password_temp)
                except:
                    pass
                with open('var.txt','w') as varfile:
                    varfile.write('out')
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
    print(retour)
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
    user=input("User :")
    password=input("Password :")
    site=input("Site :")
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


while True:
    with open('var.txt','r') as varfile:
        data=varfile.read()
        if data=="in":
            loginstatus='Logged'
        else:
            loginstatus='Not Logged'
    choix=int(input(f"[-{loginstatus}-] - 1.Flush 2.Create/Change Pass (if logged) 3.Login 4.Add 5.Content 6.Logout   :"))
    if choix==1:
        flush()
    elif choix==2:
        if 'gestionnaire_encrypted.db' in glob.glob("*.db"):
            choix_2=input('You will Destroy the Current DB. Continue ? y/n :')
            if choix_2=="y":
                os.remove('gestionnaire_encrypted.db')
            else:
                with open('var.txt','w') as varfile:
                    varfile.write('out')
                sys.exit()
        create()
        gestionnaire()
        password_user=input('Your password :')

        hash_user=Hash(password_user)
        with open('accounthash.hash','w') as hashwrite:
            hash_user.hasher()
            hashwrite.write(hash_user.hash)

        encrypt(password_user)
        sys.exit()
    elif choix==3:
        log('in')
    elif choix==4:
        add_mdp()
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