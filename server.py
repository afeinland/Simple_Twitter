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
online_users = {'u1' : False, 'u2' : False, 'u3' : False, 'u4' : False, 'u5' : False}

# User subscriptions
user_subs = {'u1' : [], 'u2' : [], 'u3' : [], 'u4' : [], 'u5' : []}

# Dictionaries for Tweets
tweets_by_user = {'u1' : [], 'u2' : [], 'u3' : [], 'u4' : [], 'u5' : []}
tweets_by_hashtag = dict()
#TODO dictionary for offline tweets, move to TBU/TBH when user logs on?
# No. All generated tweets get put into the TBU and TBH dicts. Only if a user is offline
# and a subscription of his gets a tweet should the tweet be added to the offline dict.

def printalltweetsbyuser():
    for key in tweets_by_user:
        print key
        for tweet in tweets_by_user[key]:
            print tweet



def validate_login(info):
    if info == u1+p1:
        online_users['u1'] = True
        return 'u1'
    elif info == u2+p2:
        online_users['u2'] = True
        return 'u2'
    elif info == u3+p3:
        online_users['u3'] = True
        return 'u3'
    elif info == u4+p4:
        online_users['u4'] = True
        return 'u4'
    elif info == u5+p5:
        online_users['u5'] = True
        return 'u5'
    else:
        return False

def login(conn):
    data = conn.recv(1024)
    if not data: 
        ret = False

    this_user = validate_login(data)
    if this_user is not False:
        reply = 'Welcome =) You have 0  new messages\n'
        ret = this_user
    else:
        reply = 'User not found. Closing connection'
        ret = False

    conn.sendall(reply)
    return ret

def menu(conn):
    msg = 'Choose an option:\n1 - View Offline Messsages\n2 - Edit Subscriptions\n3 - Post a Message\n4 - Hashtag Search\n5 - Logout\n\n Type \'m\' to bring up this menu.' # TODO 'm' to bring up menu
    conn.sendall(msg) # send menu to client.
    data = conn.recv(1024) # get reply from client.
    return data

def post_a_tweet(user):
# TODO tweet at a user and hashtags
# TODO also, offline tweets
    tweet = conn.recv(1024) # recv tweet from client
    tweet = user + ': ' + tweet # prefix tweet with the user who generated it.
    print tweet
    hashtag = conn.recv(1024) # recv hashtag from client
    tweets_by_user[user].append(tweet)
    tweets_by_hashtag[hashtag] = tweet
    return 0

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
    this_user = login(conn)
    if this_user is False:
        conn.close()
        return
    print this_user + ' logged in'

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
            post_a_tweet(this_user)
        elif client_command == '4': # hastag search
            reply = client_command  + ' ...OK\n'
            conn.sendall(reply)
        elif client_command == '5': # logout
            print this_user + ' logged out'
            reply = "Goodbye!"
            online_users[this_user] = False
            conn.sendall(reply)
            conn.close
            break
        else:
            printalltweetsbyuser() # debug
            break

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
