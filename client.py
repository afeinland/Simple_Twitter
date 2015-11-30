#Socket client example in python

import socket   #for sockets
import sys  #for exit

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

host = 'localhost'
port = 8889

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

#Connect to remote server
s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

def login():
    # server sends login request
    reply = s.recv(4096)
    print reply
    #login
    username = raw_input('Enter username: ')
    password = raw_input('Enter password: ')
    message = username + password

    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()


    #Server sends action request, e.g. LOGIN, or MENU, or WELCOME
        # not sure if this is a good way to do things.

login()

while 1:
    # wait for new message from server.
    reply = s.recv(4096)
    print reply

    if reply == 'Goodbye!':
        break;

    # send input to server
    user_input = raw_input('Input: ')
    s.sendall(user_input)

    if user_input == '1': # view offline messages
        print 'vom'
    elif user_input == '2': # edit subscriptions
        print 'es'
    elif user_input == '3': # post a tweet
        print 'pat'
    elif user_input == '4': # hashtag search
        print 'hts'
    elif user_input == '5': # logout
        print 'Logging out'


s.close()
