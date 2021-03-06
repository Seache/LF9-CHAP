#!/usr/bin/env python3

# import required libraries
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from random import randint
import hashlib


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# define global variables
currentToken = 0

# create list of demo user accounts
class user:  
    def __init__(self, username, password):  
        self.username = username  
        self.password = password 
   
# create list of demo users       
userList = []  
  
# appending user instances to list  
userList.append( user('demoUser1', 1234) ) 
userList.append( user('demoUser2', 5678) ) 
userList.append( user('demoUser3', 9012) )

# Create server
server = SimpleXMLRPCServer(('localhost', 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


def generateToken():
    global currentToken
    currentToken = randint(10,1000)
    return currentToken

server.register_function(generateToken, 'generateToken')
    

def challenge(username, hashValue):
    # iterate over all users and check if user with given username exists
    for user in userList:
        if user.username == username:
            # generate hash out of user password and generated token
            ownHashValue = hashlib.sha256(str(user.password).encode('utf-8') + str(currentToken).encode('utf-8')).hexdigest()
            # check if password is correct
            if(hashValue == ownHashValue):
                return 'loggedIn'
            else:
                return 'wrongPassword'
            break
    else:
        return 'userNotFound'

server.register_function(challenge, 'challenge')


def addUp(x,y):
    return x + y

server.register_function(addUp, 'addUp')


def subtract(x,y):
    return x - y

server.register_function(subtract, 'subtract')


# Run the server's main loop
server.serve_forever()
