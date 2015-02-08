#!/usr/bin/python2

# python2 because xmpp not working in python3...

import xmpp
import requests
from BeautifulSoup import BeautifulSoup
import urllib
import string

SOCIAL_SEARCH_URL = "http://127.0.0.1:5000/liveleak/"
FB_CHAT_URL = "chat.facebook.com"
CREDENTIALS_FILE = "credentials"

credentials_file = open(CREDENTIALS_FILE, 'r')
creds = credentials_file.readline()
username, passwd = creds.strip().split(':')
print username, passwd

jid = xmpp.protocol.JID(username + '@' + FB_CHAT_URL)
print jid.getDomain(), jid.getNode()
client = xmpp.Client(jid.getDomain(), debug=[])

def sanitize(s):
        s = filter(lambda x: x in string.printable, s)
        return urllib.quote(s)

def messageCB(sess,mess):
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    fromUser = mess.getFrom()

    if text is not None:
        if "liveleak.com" in text:
            text_list = text.split()
            liveleak_link = None
            for t in text_list:
                    if "liveleak.com" in t:
                            liveleak_link = t
            if liveleak_link is None:
                    print "no link found"
                    return

            title = get_live_leak_title(liveleak_link)
            title = sanitize(title)
            r = requests.get(SOCIAL_SEARCH_URL + title)
            client = xmpp.Client(jid.getDomain(), debug=[])
            client.connect(server=('chat.facebook.com',5222))
            client.auth(jid.getNode(), passwd)
            client.sendInitPresence()
            message = xmpp.Message(fromUser, r.text)
            message.setAttr('type', 'chat')
            client.send(message)
        
        else:
            print("no liveleak")


def get_live_leak_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = soup.html.head.title.string
    if "LiveLeak.com" in title:
            return title.split("LiveLeak.com - ")[1]
    else:
            return title

client.connect(server=('chat.facebook.com',5222))
client.auth(jid.getNode(), passwd)
client.sendInitPresence()
client.RegisterHandler('message',messageCB)

while 1:
    client.Process(1)
