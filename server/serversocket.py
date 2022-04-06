from genericpath import exists
import hashlib
import time
import sys
import random
import datetime
import threading
from tkinter import Y
import mariadb
import socket


connected = bool
# waits for client to connect, and then
# establishes a fluid socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
header = 64
cHeader = 2048
port = 3305
server =  socket.gethostbyname(socket.gethostname())
addr = (server, port)
format = 'utf-8'
disconnect_message = '!disconnect'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)

attemptcounter = 1
# sets up mariadb
conn = mariadb.connect(
    user="root",
    password="a",
    host="localhost",
    port=3306,
    database='accounts'
)

cur = conn.cursor()


# -------------------------------
# begin functions
# ------------------------------


def logEnable(param):
    log = True
    today = datetime.date.today()
    todayinfo = today.strftime("%d%m%Y")
    if param != '':
        logfilename = (param + str(todayinfo) + '.txt')
    elif param == '':
        logfilename = ('bankSystemLog' + str(todayinfo) + '.txt')
    directory = logfilename


def log(inp):
    print(inp)
    #creates a log file with the date, and time    
    f = open(directory, "a")
    f.write(inp)
    f.close

def error():
    print("\n[Server] : Sent Error Message.")
    return 'error'


def sessionCreator(username):
    counter = 0
    session = ''
    while True:
        if counter < 9:
            num = random.randint(0, 9)
            session = session + str(num)
            counter = counter + 1
            continue
        elif counter == 9:
            cur.execute("INSERT INTO sessions (sessionID, username) values ('" + session + "', '" + username + ");")
            return('1 ' + str(session))


#creates a secnum for nem users
def secnumCreator(sec):
    counter = 0
    secnum = ''
    while True:
        if counter < 9:
            num = random.randint(0, 9)
            secnum = secnum + str(num)
            counter = counter + 1
            continue
        elif counter == 9:
            return secnum


def userCreator(usr, pwd):
    # scans for the username
    usrCheck = bool
    pwdCheck = bool
    error = False
    users = cur.execute("SHOW username FROM accounts")
    while not error:
        for user in users:
            if user == usr:
                error = True
                break
            else:
                continue
        if not error:
            usrCheck = True
        if usrCheck:
            sesh = sessionCreator(usr)
            secnum = secnumCreator(secnum)
            cur.execute("INSERT INTO accounts(username, password, secnum, bal) values ('" + usr + "', '"
                        + pwd + "', '" + secnum + "', '0');")
            cur.execute("INSERT INTO sessions(sessionID, secnum) values ('" + sesh + "', '" + secnum + "');")
            
            return(str(sesh) + ' ' + str(secnum))
    if error:
        return False


# hasher
def hasher(hashInput):
    return str(hashlib.sha256(str(hashInput).encode('utf-8')).hexdigest())


def verify(sesh, sec):
    sessionAttempt = cur.execute("SHOW username FROM sessions WHERE sessionID='" + sesh + "';")
    accountAttempt = cur.execute("SHOW username FROM accounts WHERE secnum ='" + sec + "';")
    if sessionAttempt == accountAttempt:
        return True
    else:
        return False

def verifyUser(usr):
    try:
        username = cur.execute(
        "SHOW username FROM accounts WHERE username='" + usr + "';"
    )
    except Exception as e:
        print(str(e))
    try:
        password = cur.execute(
        "SHOW password FROM accounts WHERE username='" + usr + "';"
    )
    except Exception as e:
        print(str(e))
    if e:
        return False
    else:
        return True

def withdrawal(sesh, sec, amount):
    if verify(sesh, sec):
        currentAmount = cur.execute("SELECT bal FROM accounts WHERE secnum='" + sec + "';")
        newAmount = int(currentAmount) - int(amount)
        cur.execute("UPDATE accounts SET bal = '" + newAmount + "' WHERE secnum=" + sec + "';")
        test = cur.execute("SELECT bal FROM accounts WHERE secnum='" + sec + "';")
        if test == newAmount:
            return True
        else:
            return


def bal(sesh, sec):
    if verify(sesh, sec):
        balance = ("SELECT bal FROM accounts WHERE secnum='" + sec + "';")
        return balance
    else:
        return None


def sessionEnder(username):
    try:
        cur.exeucte(
        "DELETE FROM sessions WHERE username='" + username + "';")
    except Exception as e:
        print('')
    if not e:
        return True
    if e:
        return False

def deposit(sesh, secnum, amount):
    complete = bool
    if verify(sesh, secnum):
        currentAmount = cur.execute("SELECT bal FROM accounts WHERE secnum='" + secnum + "';")
        combinedAmount = int(currentAmount) + int(amount)
        cur.execute(
            "UPDATE accounts SET bal = '" + combinedAmount + "' WHERE secnum='" + secnum + "';"
        )
        checkAmount = cur.execute("SELECT bal FROM accounts WHERE secnum='" + secnum + "';")
        if checkAmount == combinedAmount:
            return str(checkAmount)
        else:
            cur.execute(
                "UPDATE accounts SET bal = '" + currentAmount + "' WHERE secnum='" + secnum + "';"
            )


# -----------------------y
# figure out how to store a variable that is equal to
# the position of the username and password provided
# in the database


def userCreator(username, password, secnum):
    cur.execute(
        "INSERT INTO accounts(username, password, secnum) VALUES ('" + username + "', '" + password + "', '" + int(
            secnum) + "');"
    )
    conn.commit()


messagesSent = 1


def msgHandler(msg):
    # depending on the 1st letter(command) the string will be manipulated.
    msg = msg.split()
#create new functoion where 1 is requesting a session from a already logged user
#2 is creating an account
#3 is checking if the username is available
#4-7 take the previous sequence, with section one being command, section 2 being
#usrcmd, section 3 being session, section 4 being secnum
    try:
        int(msg)
    except Exception as e:
        error()
    if int(msg[0]) == 1 or 2 or 3:
        command = msg[0]
        username = msg[1]
        password = msg[2]
        if command == '1':
            if verifyUser(username):
                return(sessionCreator(username))
        elif command == '3':
            if verifyUser(username):
                return('good')
            else:
                return('ngod')
        elif command == '2':
            userCreator(username, password)
    elif int(msg[1]) == 4 or 5 or 6:
        command = msg[1]
        usrcmd = msg[2]
        session = msg[3]
        secnum = msg[4]
        if command == '1':
            withdrawal(session, secnum, usrcmd)
        elif command == '2':
            bal(session, secnum)
        elif command == '3':
            deposit(session, usrcmd)
        else:
            return('error')
        #when ready add a transfer function.
    elif msg[1] == disconnect_message:
        if sessionEnder(msg[2]):
            cur.execute("DELETE FROM sessions WHERE username='" + str(msg[2]) + "';")
    else:
        return('error')


def msgHandler(msg):
    # depending on the 1st letter(command) the string will be manipulated.
    msg = msg.split()
#create new functoion where 1 is requesting a session from a already logged user
#2 is creating an account
#3 is checking if the username is available
#4-7 take the previous sequence, with section one being command, section 2 being
#usrcmd, section 3 being session, section 4 being secnum
    try:
        int(msg)
    except Exception as e:
        error()
    if int(msg[0]) == 1 or 2 or 3:
        command = msg[0]
        username = msg[1]
        password = msg[2]
        if command == '1':
            if verifyUser(username):
                return sessionCreator(username)
        elif command == '3':
            if verifyUser(username):
                return 'good'
            else:
                return 'ngod'
        elif command == '2':
            userCreator(username, password)
    elif int(msg[1]) == 4 or 5 or 6:
        command = msg[1]
        usrcmd = msg[2]
        session = msg[3]
        secnum = msg[4]
        if command == '1':
            withdrawal(session, secnum, usrcmd)
        elif command == '2':
            bal(session, secnum)
        elif command == '3':
            deposit(session, usrcmd)
        else:
            return 'error'
        #when ready add a transfer function.
    elif msg[1] == disconnect_message:
        if sessionEnder(msg[2]):
            cur.execute("DELETE FROM sessions WHERE username='" + str(msg[2]) + "';")
    else:
        return 'error'


#handles socket clients
def handle_client(connection, address):
    print(f"[new connection]: " + str(address) + " has connected.")
    connected = True
    while connected:
        msg_length = connection.recv(header).decode(format)
        if msg_length:
            msg_length = int(msg_length)
            declaration = connection.recv(msg_length).decode(format)
            msg = (declaration)
            handled = msgHandler(msg)
            connection.send(handled.encode(format))
            print(f"[Server]: Sent: {handled} \n - Awaiting response...")

    connection.close()


#starts the server
def start():
    #queries user to log
    logQ()
    #listens for connections
    s.listen()
    log(f"Server is listening on '{str(server)}:{str(port)}'.")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        log(f"[connections] : {threading.activeCount() - 1}")
        

def logQ():    
    while True:
        logQ = input("Would you like the server to log to a file?")
        if logQ.lower() == 'yes' or 'y':
            logQ2 = input("What would you like to name the file? (We'll include the date for you)(Press ENTER to skip) ")
            logEnable(logQ2)
            print("Started logging at " + str(datetime.datetime.now()))
            break
        elif logQ.lower() == 'no' or 'n':
            print("Okay, continuing.")
            break
        else:
            print("Improper syntax, try again with 'yes', or 'no'")
            continue
#starts the main server listener
start()