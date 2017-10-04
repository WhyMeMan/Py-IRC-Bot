import sys
import socket
from irc import *
import os
import random
import datetime as dt

def main():
    irc = IRC()
    channel = "#azami-py-bot"
    irc.connect("irc.heuxe.org", channel, "AzamiPYBot")



    while True:
        text = irc.get_text()
        print(text)

        if "PRIVMSG" in text:
            split = text.split()
            currentChannel = split[2]
            command = text.split(' :', 1)[1]
            user = split[0].split("!")[0].replace(":", "")
            hostname =  text.split("@")[1].split()[0]

            if (command.startswith(".")):
                #Check Authentication
                authFile = open("auth.txt", "r")
                authResponse = "Not Authorized"
                for line in authFile:
                    if line[:-1] == hostname:
                        authResponse = "Authorized"
                        break
                authFile.close()
                authorized = authResponse == "Authorized"

                if command.startswith(".auth"):
                    if "status" in command:
                        irc.send(currentChannel, f'You are {authResponse} to use me')

                if authorized:
                    if command.startswith(".auth remove"):
                        userToRemove = command.split()[2] + "\n"
                        authFile = open("auth.txt", "r")
                        userList = authFile.readlines()
                        if userToRemove in userList:
                            userList.remove(userToRemove)
                        authFile.close()
                        authFile = open("auth.txt", "w")
                        authFile.writelines(userList)
                        authFile.close()
                        irc.send(currentChannel, f'New Authorization List: {userList}')
                    if command.startswith(".auth list"):
                        authFile = open("auth.txt", "r")
                        tmpList = authFile.readLines()
                        userList = map(lambda each:each.strip("\n"), tmpList)
                        irc.send(currentChannel, )
                    if command.startswith(".raw"):
                        irc.raw(text.split('.raw ', 1)[1])
                    if command.startswith(".register"):
                        irc.register()
                    if command.startswith(".identify"):
                        irc.identify()
                    if command.startswith(".quit"):
                        irc.quit()
                    if command.startswith(".debug"):
                        irc.debug(currentChannel, user, command)
                    if command.startswith(".ping"):
                        irc.send(currentChannel, "Pong")
                    if command.startswith(".hostname"):
                        irc.send(currentChannel, hostname)
                    if command.startswith(".eval"):
                        evalAttempt = command.replace(".eval ", "")
                        try:
                            n1 = dt.datetime.now()
                            evalResponse = eval(evalAttempt)
                            n2 = dt.datetime.now()
                            elapsed = (n2 - n1).microseconds
                            irc.send(currentChannel, f'{evalResponse} ({elapsed}µs)')
                        except:
                            irc.send(currentChannel, f'Error parsing eval: {evalAttempt}')
                    if command.startswith(".exec"):
                        execAttempt = command.replace(".exec ", "")
                        try:
                            n1 = dt.datetime.now()
                            execResponse = exec(execAttempt)
                            n2 = dt.datetime.now()
                            elapsed = (n2 - n1).microseconds
                            irc.send(currentChannel, f'Executed ({elapsed}µs)')
                        except:
                            irc.send(currentChannel, f'Error parsing exec: {execAttempt}')
                else:
                    irc.send(currentChannel, "You do not have permission to do this.")



if __name__ == '__main__':
    sys.exit(main())