import socket
import sys
from thread import *



# User Accounts
u1 = 'user1'
p1 = 'pass1'
u2 = 'user2'
p2 = 'pass2'
u3 = 'user3'
p3 = 'pass3'
u4 = 'user4'
p4 = 'pass4'
u5 = 'user5'
p5 = 'pass5'

def validate_login(info):
    if info == u1+p1:
        return True
    elif info == u2+p2:
        return True
    elif info == u3+p3:
        return True
    elif info == u4+p4:
        return True
    elif info == u5+p5:
        return True
    else:
        return False

def login(conn):
    data = conn.recv(1024)
    if not data: 
        ret = False

    if validate_login(data) is True:
        reply = 'Welcome =) You have 0  new messages\n'
        ret = True
    else:
        reply = 'User not found. Closing connection'
        ret = False

    conn.sendall(reply)
    return ret

def menu(conn):
    msg = 'Choose an option:\n1 - View Offline Messsages\n2 - Edit Subscriptions\n3 - Post a Message\n4 - Hashtag Search\n5 - Logout\n'
    conn.sendall(msg) # send menu to client.
    data = conn.recv(1024) # get reply from client.
    return data

# Socket creation, bind, listen
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'


def clientthread(conn):
    # Client login
    conn.send('Welcome to the server. Please log in.\n') #send only takes string
    if login(conn) is False:
        conn.close()
        return

    # Client login successful, keep connection open until user logout.
    while True:

        client_command = menu(conn)


        if client_command == '1': # view offline messages
            reply = client_command  + ' ...OK\n'
            conn.sendall(reply)
        elif client_command == '2': # edit subscriptions
            reply = client_command  + ' ...OK\n'
            conn.sendall(reply)
        elif client_command == '3': # post a tweet
            reply = client_command  + ' ...OK\n'
            conn.sendall(reply)
        elif client_command == '4': # hastag search
            reply = client_command  + ' ...OK\n'
            conn.sendall(reply)
        elif client_command == '5': # logout
            reply = "Goodbye!"
            conn.sendall(reply)
            conn.close
            break
        else:
            conn.close()
            break

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
