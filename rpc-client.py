#!/usr/bin/env python3

import xmlrpc.server
import xmlrpc.client
from random import randint
import hashlib

s = xmlrpc.client.ServerProxy('http://localhost:8000')

token = s.generateToken()
print(token)

username = input("Enter your username: ")
password = input("Enter your password: ")
hashValue = hashlib.sha256(str(password).encode('utf-8') + str(token).encode('utf-8')).hexdigest()
print(hashValue)
print (s.challenge(username, hashValue))

print (s.pow(2,3))  # Returns 2**3 = 8
print (s.add(2,3))  # Returns 5
print (s.div(5,2))  # Returns 5//2 = 2

# Print list of available methods
print (s.system.listMethods())
