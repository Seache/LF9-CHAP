#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from random import randint
import hashlib


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

currentToken = 0
userPassword = 12345678
# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

def generateToken():
    global currentToken
    currentToken = randint(10,1000)
    return currentToken

server.register_function(generateToken, 'generateToken')
    

def challenge(hashValue):
    ownHashValue = hashlib.sha256(str(userPassword).encode('utf-8') + str(currentToken).encode('utf-8')).hexdigest()
    print(ownHashValue)
    if(hashValue == ownHashValue):
        return "Successfully logged in"
    else:
        return "Could not log in"

server.register_function(challenge, 'challenge')

# Register a function under a different name
def adder_function(x,y):
    return x + y

server.register_function(adder_function, 'add')

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class MyFuncs:
    def div(self, x, y):
        return x // y

server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
