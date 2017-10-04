import socket
import sys
import time

class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def raw(self, raw):
        print("Raw Command:\n%s" % raw)
        self.irc.send(raw.encode("UTF-8"))

    def debug(self, channel, user, command):
        to_send = f'Channel: {channel} User: {user} Command: {command}\n'
        print(to_send)
        self.send(channel, to_send)

    def quit(self):
        print ("Quitting")
        to_send = "QUIT Exit by Command\n"
        print(to_send)
        self.raw(to_send)
        sys.exit(quit())

    def register(self):
        print("Registering")
        to_send = "PRIVMSG nickserv :register null123456Null azamibots@gmail.com\n"
        print(to_send)
        self.raw(to_send)

    def identify(self):
        print("Identifying")
        to_send = "PRIVMSG nickserv :identify null123456Null\n"
        print(to_send)
        self.raw(to_send)

    def send(self, chan, msg):
        to_send = "PRIVMSG " + chan + " :" + msg + "\n"
        print(to_send)
        self.irc.send(to_send.encode("UTF-8"))

    def connect(self, server, channel, botnick):
        # defines the socket
        print("connecting to:" + server)
        self.irc.connect((server, 6667))  # connects to the server
        password = "null123456Null"
        time.sleep(2)

        self.irc.send(("PASS %s\n" % (password)).encode("UTF-8"))
        self.irc.send(("USER " + botnick + " " + botnick + " " + botnick + " :Azami-Py3-6-12-Bot\n").encode("UTF-8"))
        self.irc.send(("NICK " + botnick + "\n").encode("UTF-8"))
        self.irc.send(("JOIN " + channel + "\n").encode("UTF-8"))

    def get_text(self):
        text = self.irc.recv(2040).decode()  # receive the text

        if text.find('PING') != -1:
            self.irc.send(('PONG ' + text.split()[1] + '\r\n').encode("UTF-8"))

        return text