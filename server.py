import socket
import sys
from thread import *
from collections import defaultdict




# User accounts
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
online_users = {'u1' : False, 'u2' : False, 'u3' : False, 'u4' : False, 'u5' : False, 'null_user' : False}

# User subscriptions
user_subs = {'u1' : [], 'u2' : [], 'u3' : [], 'u4' : [], 'u5' : []}

# Connections to each user
user_conns = {'u1' : 0, 'u2' : 0, 'u3' : 0, 'u4' : 0, 'u5' : 0}

# Dictionaries/Lists for Tweets
tweets_by_user = {'u1' : [], 'u2' : [], 'u3' : [], 'u4' : [], 'u5' : []}
tweets_by_hashtag = defaultdict(list)
offline_tweets = {'u1' : [], 'u2' : [], 'u3' : [], 'u4' : [], 'u5' : []} # tweets by u1's subscriptions while u1 was offline.




def printalltweetsbyuser(): #debug
    for key in tweets_by_user:
        print key
        for tweet in tweets_by_user[key]:
            print tweet

def printalltweetsbyht(): #debug
    for key in tweets_by_hashtag:
        print key
        for tweet in tweets_by_hashtag[key]:
            print tweet

def viewsubs(): #debug
    for key in user_subs:
        print 'subs for user ' + key + ':'
        for sub in user_subs[key]:
            print sub

def isonline(user):
    return online_users[user]


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
        reply = 'Welcome =) You have ' + str(len(offline_tweets[this_user])) + ' new messages\n'
        user_conns[this_user] = conn
        ret = this_user
    else:
        reply = 'User not found. Closing connection'
        ret = False

    conn.sendall(reply)
    return ret

def menu(conn):
    msg = '\nChoose an option:\n1 - View Offline Messsages\n2 - Edit Subscriptions\n3 - Post a Message\n4 - Hashtag Search\n5 - Logout\n\n'
    conn.sendall(msg) # send menu to client.
    data = conn.recv(1024) # get reply from client.
    return data

def add_sub(user, conn):
    selected_user = 'null_user'
    conn.sendall('Which user would you like to add?')
    selected_user = conn.recv(1024)
    user_subs[user].append(selected_user)
    print 'added user ' + selected_user

def remove_sub(user, conn):
    current_subs = user_subs[user]
    conn.sendall('Choose a user' + ''.join(current_subs))
    user_to_remove = conn.recv(1024)
    user_subs[user].remove(user_to_remove)

def edit_subs(user, conn):
    conn.sendall('\nAdd (a) or remove (r) a subscription?\n')    # ask client, add or remove a sub?
    reply = conn.recv(1024)
    if reply == 'a':
        add_sub(user, conn)
    else:
        remove_sub(user, conn)


def post_a_tweet(user, conn):
    tweet = conn.recv(1024) # recv tweet from client
   
    #TODO check user_subs for user. For each offline user who subs to this user, also store the tweet in that user's offline tweet dict.
    for key in user_subs:
        if key == user:
            continue # user can't subscribe to themself
        elif isonline(key) is False:
            print key + ' is offline.'
            for sub in user_subs[key]:
                if sub == user: # if a user is subscribed to this user
                    print key + ' is offline and subscribed to ' + user
                    offline_tweets[key].append(tweet)

    tweet = user + ': ' + tweet # prefix tweet with the user who generated it.
    hashtag = conn.recv(1024) # recv hashtag from client
    print 'New tweet/hashtag: ' + tweet + '/' + hashtag
    tweets_by_user[user].append(tweet)
    tweets_by_hashtag[hashtag].append(tweet)

def get_tweets_by_ht(ht): # returns list of tweets with hashtag ht
    ret = []
    for value in tweets_by_hashtag[ht]:
        ret.append(value)
    return ret

def hashtag_search(conn): # sends to client at connection conn a list of tweets with client defined hashtag
# ask client for ht
    ht = conn.recv(1024)
# search for the ht
    tweets = get_tweets_by_ht(ht)
# send tweets to client
    if not tweets:
        conn.sendall('Hashtag not found\n')
    else:
        conn.sendall(''.join(tweets))
    
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
            edit_subs(this_user, conn)
        elif client_command == '3': # post a tweet
            post_a_tweet(this_user, conn)
        elif client_command == '4': # hastag search
            hashtag_search(conn)
        elif client_command == '5': # logout
            print this_user + ' logged out'
            reply = "Goodbye!"
            online_users[this_user] = False
            conn.sendall(reply)
            conn.close
            break
        elif client_command == 'pbu':
            printalltweetsbyuser() # debug
        elif client_command == 'pbh':
            printalltweetsbyht() # debug
        elif client_command == 'vs':
            viewsubs() #debug
        else:
            conn.sendall('Invalid option')
            

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
