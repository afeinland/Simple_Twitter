#Socket client example in python

import socket   #for sockets
import sys  #for exit
import select

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'

host = '10.0.0.4'
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

    reply = s.recv(4096) # recv login reply from server
    print 'login reply: ' + reply

def post_a_tweet():
    tweet = raw_input('Tweet text: ')
    s.sendall(tweet)
    hashtags = raw_input('Hashtag: ')
    s.sendall(hashtags)

def hashtag_search():
    ht = raw_input('Enter hashtag to search: ')
    s.sendall(ht) # send hashtag to server
    tweets = s.recv(4096) # server returns lsit of tweets with that hashtag
    print tweets

def add_sub():
    reply = s.recv(4096) # server asks for a user to add or remove.
    print reply
    selected_user = raw_input('User: ')
    s.sendall(selected_user)

def remove_sub():
    reply = s.recv(4096) # server asks for a user to add or remove.
    print reply
    selected_user = raw_input('User: ')
    s.sendall(selected_user)

def edit_subs():
    reply = s.recv(4096) # server asks whether to add or remove a user.
    print reply
    reply = raw_input('Reply: ')
    s.sendall(reply)
    if reply == 'a':
        add_sub()
    elif reply == 'r':
        remove_sub()


def view_offline_msgs():
    msgs = s.recv(4096)
    print msgs

login()

while 1:
    # wait for new message from server.
    reply = s.recv(4096)
    print 'reply: ' + reply

    if reply == 'Goodbye!':
        break;


    # send input to server
    user_input = raw_input('Option: ')
    s.sendall(user_input) # send client's menu option to server

    # do local work based on menu option. Server should be waiting for
        # client to send the appropriate data given the selected menu option.
    if user_input == '1': # view offline messages
        view_offline_msgs()
    elif user_input == '2': # edit subscriptions
        edit_subs()
    elif user_input == '3': # post a tweet
        post_a_tweet()
    elif user_input == '4': # hashtag search
        hashtag_search()
    elif user_input == '5':
        tweet = s.recv(4096)
        print tweet
    elif user_input == '6': # logout
        print 'Logging out'
    elif user_input == 'pbu' or user_input == 'pbh' or user_input == 'vs': # debug
        continue
    elif user_input == 'messagecount':
        cnt = s.recv(4096)
        print cnt
    else:
        reply = s.recv(4096)
        print reply


s.close()
