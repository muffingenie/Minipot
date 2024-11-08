80#minihoneypot
import socket
import datetime 
import smtplib
import time 
import sys
import sqlite3

################## BANNER CONFIGURATION ##########################
default_banner = ('no data transmitted\n')
http = ('HTTP/1.0 200 OK\n')
pureftpd = """220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\n
220-You are user number 2 of 80 allowed.\n
220-Local time is now %s. Server port: 21.\n
220-This is a private system - No anonymous login\n
220-IPv6 connections are also welcome on this server\n.
220 You will be disconnected after 15 minute...\n)"""%(time.ctime())
AD = ('LDAP:\n NamingContexts: dc=Aerospace,dc=local \n SupportedControl: \n 1.2.826.0.1.3344810.2.3 \n 1.2.840.113556.1.4.319 \n 1.3.6.1.1.12\n  1.3.6.1.1.13.1 \n 1.3.6.1.1.13.2 \n 1.3.6.1.4.1.4203.1.10.1 \n 2.16.840.1.113730.3.4.18\n  2.16.840.1.113730.3.4.2 \n  SupportedExtension: \n 1.3.6.1.1.8 \n 1.3.6.1.4.1.1466.20037 \n 1.3.6.1.4.1.4203.1.11.1 \n 1.3.6.1.4.1.4203.1.11.3 \n SupportedLDAPVersion: 3 \n SupportedSASLMechanisms: \n CRAM-MD5 \n DIGEST-MD5 \n  NTLM \n SubschemaSubentry: cn=Aerospace\n')

################## INTERACTIONS ##########################
fakeshell = ('$')
root_welcome = ('root\n')
pwd = ('/bin\n')
ls_cmd = """\[		dd		ksh		pax		stty\n
bash		df		launchctl	ps		sync\n
cat		echo		link		pwd		tcsh\n
chmod		ed		ln		rm		test\n
cp		expr		ls		rmdir		unlink\n
csh		hostname	mkdir		sh		wait4path\n
date		kill		mv		sleep		zsh\n

    """
user_error = ("error")

################# function to save connections to minipot ###########


conn = sqlite3.connect('minipot.db')
c = conn.cursor()

c.execute("""

CREATE TABLE IF NOT EXISTS honey(
    Time TEXT, 
    IP TEXT,
    Data TEXT

)
""")
          
def WriteDB(Date_attack,Ip_attack,Data_attack):
    c.execute('INSERT INTO honey VALUES (?,?,?)',((Date_attack),(Ip_attack),(Data_attack)))
    conn.commit()


################ MINIPOT code ############
print("""
   __  ____      _           __ 
  /  |/  (_)__  (_)__  ___  / /_
 / /|_/ / / _ \/ / _ \/ _ \/ __/
/_/  /_/_/_//_/_/ .__/\___/\__/ 
               /_/              \n""")

print('[+] Starting MiniPot v1\n')
print ('[?] enter a port number:')
port = int(input())
if (port < 1) or (port > 65535):
	print("Invalid port number")
   
print("""[?] Choose the banner to display:
[-]default
[-]http
[-]pureftpd
[-]AD
[-]Custom
>
""")
banner_selected = input()

if banner_selected.lower() == "custom":

    print('[?] Type your custom banner here:')
    custom_banner = input()
    

while True:
    
    try:
#### Socket's set up and config ###


        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        serversocket.bind(('', port)) # bind socket 
        serversocket.listen(5) # listen
        print('[+] MiniPot is up and running')
        print('Listening on port %s'%(port))

        (clientsocket, address) = serversocket.accept() # accept external connexion
        ipattacker = address 
        ServerTime= "%s"%datetime.datetime.now()

###### banner to be send #####

        if banner_selected.lower() == "http" :
            banner_tosend = http.encode()
            clientsocket.send(banner_tosend)

        elif "pureftpd" in banner_selected.lower():
            banner_tosend = pureftpd.encode()
            clientsocket.send(banner_tosend)
 
        elif banner_selected.lower() == "AD" :
            banner_tosend = AD.encode()
            clientsocket.send(banner_tosend)

        elif banner_selected.lower() == "custom":
            banner_tosend = custom_banner.encode()
            clientsocket.send(banner_tosend)
        
        else:

            banner_tosend = default_banner.encode()
            clientsocket.send(banner_tosend)
        
        #clientsocket.send(banner_tosend)
        clientsocket.send(fakeshell.encode())
        print('Connexion from: %s at %s'%(ipattacker, ServerTime))
    
        #clientsocket.close()

#### Receive and interact with cmd #####

        while True:
            data = ('')
            data = clientsocket.recv(1024)
            #print(data)
            total_data= []
            total_data.append(data)
            data_export = str(total_data)
            command =(''.join(data_export))

            if "whoami" in command:
                root_welcome_tosend = root_welcome.encode()
                clientsocket.send(root_welcome_tosend)

            elif "pwd" in command:
                pwd_tosend = pwd.encode()
                clientsocket.send(pwd_tosend)

            elif ("ls") in command:
                ls_tosend = ls_cmd.encode()
                clientsocket.send(ls_tosend)

            else:
                error_tosend = user_error.encode()
                clientsocket.send(error_tosend)



            print(''.join(data_export))
            #writeLog(ipattacker, data_export)
           

            Dateofattack = str(ServerTime)
            Ipofattack = str(ipattacker)
            Dataofattack = str(data_export)
            
            WriteDB(Dateofattack, Ipofattack, Dataofattack)
            
           
        
            #clientsocket.close()
         
        
    except socket.error:
        clientsocket.close()
        print('[-] Minipot has encountered an error')
        #sys.exit()



    #writeLog(ipattacker, data_export)
    #serversocket.settimeout(10) 
    

