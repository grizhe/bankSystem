#still for fun :)! Program created by Grizhe... DISCLAIMER : any correlation to real world people or real world bank accounts is unintentional, and the entire project I am creating / have created is for my own personal enjoyment. Any affiliation to the real world is unintentional, and completely coincidential. This program is not used to earn money.
#ACTUAL CODE INFO Until said otherwise, this is all function declaration. The main part of the program is towards the bottom.

import hashlib
from sys import *
from time import *


#account schematic ----------------------------------
account = dict()
account[key].append()
		
#disband *kill switch*
def disband():
  print("Program shutdown via internal kill switch.")
  sys.exit()

#codeerror---------------------------------------
def codeerror():
	print(
	    "There was an error in the code, please contact Grizhe via discord: grizhe#1737"
	)


#username is kyelw(sha256) num is 294495, bal is starting at $1600, sc is 5231
#TESTER ACCOUNT



#hash function----------------------------------------
def hash(hashInput):
  return str(hashlib.sha256(str(hashInput).encode('utf-8')).hexdigest)
   

#grizhe number encryption ---------------------------

def numencrypt(numinp):
  int(numinp)
  numinp +1 -3 /6.2356622 * 3.543970 * 15.193241
  return numinp


#login verification -----------------------------
notuserlist = []
def usrlogin(username):
	for user in account.usern:
		if hash(username) == user:
		  return True
		elif hash(username) != account:
		  user.append(notuserlist)

notuserlist = []
def usrlogin(username):
  for user in account.usern:
    if hash(username) == user:
      return True
    elif hash(username) != account:
      user.append(notuserlist)
    elif amount(account.usern) <= 0:
      return False


#Security Code Verifier ----------------------------
def seccode(securitycode):
	tries = 0
	#insert security verifier here


#--------------------------------------------
#MAIN SECTION OF program
#--------------------------------------------
userkey = False
print(
    "Hello, welcome to grizhe's banking system, please input your username. Have your security code on hand as well."
)
userkey = False
userhash = input(".:.")
usernameSignin = True
while usernameSignin == True:
  #will limit the amount of attempts someone has to sign in
  usernameSigninAttempts = 0
  while usernameSigninAttempts != 3:
    #checks if the username matches any logins
    if usrlogin(userhash) == True:
      print("Welcome, " + account.name.title())
      userkey = True
      break
    #inccorect login statement
    elif usrlogin(userhash) == False:
      print("Incorrect username, please try again. Attempt #" + str(usernameSigninAttempts) + "/3.")
      usernameSigninAttempts + 1
      continue
      #fallback
    else:
      disband()
  #if statement for the secnario that someone DOES attmept too many times
  if usernameSigninAttempts == 3:
    print("I am sorry, you tried too many times. Shutting down program, please contact grizhe.")
    disband()
  elif userkey == True:
    continue
  else:
    disband()
  