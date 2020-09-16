#!/usr/bin/env python3

import xmlrpc.server
import xmlrpc.client
from random import randint
import hashlib

s = xmlrpc.client.ServerProxy('http://localhost:8000')

# generate token to combine with password
token = s.generateToken()

# request username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# generate hash value out of password and token
hashValue = hashlib.sha256(str(password).encode('utf-8') + str(token).encode('utf-8')).hexdigest()

# check hash value in combination with username
status = s.challenge(username, hashValue)

# method to list available functions for authenticated users
def showActions():
    print("Moegliche Aktionen als authentifizierter Nutzer:")
    print("1. Add up two figures")
    print("2. Subtract two figures")
    print("3. Logout")
    action = int(input("Please enter the number of the action you want to execute:"))
    if action == 1:
        firstFigure = int(input("Enter first figure:"))
        secondFigure = int(input("Enter second figure:"))
        result = s.addUp(firstFigure, secondFigure)
        print("Result: " + str(result) + "\n")
        showActions()
    elif action == 2:
        firstFigure = int(input("Enter first figure:"))
        secondFigure = int(input("Enter second figure:"))
        result = s.subtract(firstFigure, secondFigure)
        print("Result: " + str(result) + "\n")
        showActions()
    elif action == 3:
        print("Logged out")
    else:
        print("Action does not exists")
        showActions()

# check status
if status == "loggedIn":
    showActions()
elif status == "wrongPassword":
    print("Wrong password")
elif status == "userNotFound":
    print("User not found")
else:
    print("Error")
