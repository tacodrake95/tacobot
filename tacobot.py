import socket
import random
import sys
import time
import os
import string
import datetime
import ssl
import json

import os.path

class gvars:
    
    def __init__(self):
        self.flags = ""
        
class tacobot:

    def __init__(self):
        if sys.platform == "win32":
            pathSep = "\\"
        else:
            pathSep = "/"

        os.chdir(os.path.abspath(sys.argv[0]).rsplit(pathSep, 1)[0])

        self.bnick = "tacobot"
        self.master = "taco"
        self.commands = {
                        "raw" : self.raw,
                        "ping" : self.ping,
                        "quit" : self.reset,
                        "reset" : self.reset,
                        "getcwd" : self.cwd,
                        "give" : self.give,
                        "inventory" : self.inv,
                        "chansay" : self.chanSay,
                        "choose" : self.choose,
                        "part" : self.part,
                        "join" : self.join,
                        "nick" : self.nickChange,
                        "commands" : self.commands,
                        "log" : self.islogging,
                        "action" : self.do
                        }
        self.host = "irc.subluminal.net"
        self.port = 6697
        self.ident = "tacobot"
        self.name = "Taco Bell Bot"
        self.master = ["taco", "tacopanda95", "svkampen", "svk", "me"]
        self.bufferFile = ""
        self.s = socket.socket( )
        self.s = ssl.wrap_socket(self.s)
        self.writelogs = True

        #init command vars
        self.command = ""
        self.longArg = ""
        self.longMsg = ""
        self.chan = ""
        self.arg = []
        self.nick = ""
        self.hasArgs = False

        self.pwd = open("%s%spwd.dat" % (os.getcwd(), pathSep)).readline().rstrip("\n")

        file = open("inventory.json", "r")

        self.inventory = json.load(file)
        
        file.close()
        
    def connect(self):
        self.s.connect((self.host, self.port))

        self.bufferFile = self.s.makefile() 

        self.send("USER %s %s %s :%s" % (self.ident, self.host, self.bnick, self.name))
        self.send("NICK %s" % self.bnick)


    def parse(self, msg):
        splitmsg = msg.split(" ", 2)
        info = {"method": splitmsg[1], "host": splitmsg[0][1:], "arg": splitmsg[2]}
        return info


    def isMaster(self, nick):
        if nick in self.master and self.getAuth(nick):
            return True
        else:
            self.msg("%s: you're not my dad" % nick, self.chan)
            return False
        
    def isInChannel(self, nick, chan):
        self.send("NAMES %s" % chan)
        line = {"method" : "NOMETHOD"}
        names = ""
        while line["method"] != "353":
            try:
                line = self.bufferFile.readline().rstrip("\r\n")
            except UnicodeDecodeError:
                line = "NOMETHOD nouser!nohost :nomsg"
            if line.find("PING") == 0:
               self.send(line.replace("PING", "PONG", 1))
               line = {"method" : "NOMETHOD"}
            else:
                line = self.parse(line)
        
        names = line["arg"].rsplit(":", 1)[1].strip().lower()
        names = ([i.lstrip(" %s" % globals.flags) for i in names.split()])
        return nick in names

    def getNick(self, host):
        return host.split("!", 1)[0]

    def action(self, msg, chan):
        self.send("PRIVMSG %s :\x01ACTION %s\x01" % (chan, msg))
        text = "%s *%s %s" % (str(datetime.datetime.now().time()).split(".")[0], self.bnick, msg)
        self.log(chan, text)

    def getAuth(self, nick):
        self.send("PRIVMSG NickServ ACC %s" % nick)
        line = {"method" : "NOMETHOD"}
        while line["method"] != "NOTICE":
            line = self.bufferFile.readline().rstrip("\r\n")
            if line.find("PING") == 0:
               self.send(line.replace("PING", "PONG", 1))
               line = {"method" : "NOMETHOD"}
            else:
                line = self.parse(line)
             
        self.args = line["arg"].split()
        print(line["arg"])
        return(self.args[1].strip(":") in self.master and self.args[2]== "ACC" and self.args[3] == "3")

    def toggle(self, boolean):
        try:
            return not boolean
        except:
            print("Not a boolean")
            return boolean
    
    def log(self, chan, text):
        if b.writelogs:
            log = open("%s_log.log" % chan.strip(), "a")
            log.write("%s\n" % text)
            log.close()

    def msg(self, msg, chan):
        self.send("PRIVMSG %s :\x0310%s" % (chan, msg))
        text = "%s <%s> %s" % (str(datetime.datetime.now().time()).split(".")[0], self.bnick, msg)
        self.log(chan, text)


    def send(self, msg):
        print(msg)
        self.s.sendall(bytes("%s\r\n" % msg, "UTF-8"))

    def islogging(self):
        if self.isMaster(self.nick):
            if self.hasArgs:
                if self.arg[0].lower() == "false":
                    self.writelogs = False
                elif self.arg[0].lower() == "true":
                    self.writelogs = True
            else:
                self.writelogs = self.toggle(self.writelogs)
    
            if self.writelogs:
                self.msg("Writing to logs", self.chan)
            else:
                self.msg("Not writing to logs", self.chan)
    
    def do(self):
        if self.hasArgs:
            self.action(self.longArg, self.chan)

    def ping(self):
        if self.hasArgs:
            self.msg("Pong %s" % self.longArg, self.chan)
        else:
            self.msg("Pong", self.chan)

    def reset(self):
        if self.isMaster(self.nick):
            self.send("QUIT :Quitting")
            print("Quitting.")
            self.s.close()
            self.save()
            sys.exit()

    def cwd(self):
        self.msg(os.getcwd(), self.chan)

    def isANum(self, num):
        if isinstance(num, int):
            return True
        else:
            try:
                a = int(num)
            except:
                return False
            else:
                return True

    def raw(self):
        if self.isMaster(self.nick):
           self. send(self.longArg)

    def give(self):
        
        fromNick = self.nick.lower()
        if self.hasArgs:
            toNick = self.arg[0].lower()

        if not (fromNick in self.inventory.keys()):
            self.inventory[fromNick] = {"dong": {"amount": 1}}
            self.save()
            
        if self.hasArgs:
            if self.isInChannel(toNick, self.chan):
                if not (toNick in self.inventory.keys()):
                    self.inventory[toNick] = {"dong": {"amount": 1}}
                    self.save()
                    
                if len(self.arg) >= 2:
                    if self.isANum(self.arg[1]):
                        if len(self.arg) >= 3:
                            item = self.longArg.split(" ", 2)[2]
                            amount = int(self.arg[1])
                        else:
                            amount = 0
                    else:
                        if self.arg[1].lower() == "a" or self.arg[1].lower() == "an":
                            item = self.longArg.split(" ", 2)[2]
                        else:
                            item = self.longArg.split(" ", 1)[1]
                        amount = 1

                    if amount > 0:
                        if item in self.inventory[fromNick].keys():
                            if self.inventory[fromNick][item]["amount"] >= amount:
                                self.msg("%s: you have given %s %s %s." % (self.nick, self.arg[0], amount, item), self.chan)
                                self.inventory[fromNick][item]["amount"] -= amount
                                if item in self.inventory[toNick].keys():
                                    self.inventory[toNick][item]["amount"] += amount
                                else:
                                    self.inventory[toNick][item]= {"amount": amount}
                                self.save()
                            else:
                                self.msg("%s: You don't have enough %s" %(fromNick, item), self.chan)
                        else:
                            self.msg("%s: You don't have any %s." % (fromNick, item), self.chan)
                    else:
                        self.msg("%s: Format incorrect or invalid number, try again." % fromNick, self.chan)
                else:
                    self.msg("%s: Not enough arguments." % fromNick, self.chan)
            else:
                self.msg("%s: %s is not in the channel." % (fromNick, toNick), self.chan)
    
    def commands(self):
        self.send("NOTICE %s :Commands:" % self.nick)
        commands = ""
        for key in self.commands:
            commands = "%s %s" % (commands, key)
            
        commands = commands.strip().replace(" ", ", ")
        self.send("NOTICE %s :%s" % (self.nick, commands))
    
    def inv(self):

        self.nick = self.nick.lower()

        if not (self.nick in self.inventory.keys()):
            self.inventory[self.nick] = {"dong": {"amount": 1}}
            self.save()

        for key in list(self.inventory[self.nick].keys()):
            if self.inventory[self.nick][key]["amount"] == 0:
                del(self.inventory[self.nick][key])
                
        if len(self.inventory[self.nick]) == 1:
            for key in self.inventory[self.nick]:
                args = "%s: you have %s %s in your inventory" % (self.nick, self.inventory[self.nick][key]["amount"], key)
        elif len(self.inventory[self.nick]) == 2:
            i = 1
            for key in self.inventory[self.nick]:
                if i == 1:
                    args = "%s: you have %s %s" % (self.nick, self.inventory[self.nick][key]["amount"], key)
                else:
                    args = "%s and %s %s in your inventory" % (args, self.inventory[self.nick][key]["amount"], key)
                i += 1                            
        else:
            i = 2
            for key in self.inventory[self.nick]:
                if i == 2:
                    args = "%s: you have %s %s," % (self.nick, self.inventory[self.nick][key]["amount"], key)
                elif i <= len(self.inventory[self.nick]):
                    args = "%s %s %s," % (args, self.inventory[self.nick][key]["amount"], key)
                else:
                    args = "%s and %s %s in your inventory" % (args, self.inventory[self.nick][key]["amount"], key)
                i += 1
        try:
            self.msg(args, self.chan)
        except Exception as e:
            print(e)

    def join(self):
        if self.hasArgs and self.isMaster:
            self.send("JOIN %s" % self.arg[0])

    def part(self):
        if self.isMaster:
            if self.hasArgs:
                if len(self.arg) == 1:
                    if self.arg[0] == "":
                        args = self.chan
                    else:
                        args = self.arg[0]
                elif len(self.arg) >= 2:
                    lArg = self.longArg.split(" ", 1)[1]
                    args = "%s :%s" % (self.arg[0], lArg)
            else:
                args = self.chan
                        
            self.send("PART %s" % args)

    def chanSay(self):
        if self.isMaster(self.nick):
            self.msg(self.longArg.split(" ", 1)[1], self.arg[0])
    
    def nickChange(self):
        if self.isMaster(self.nick) and self.hasArgs:
            self.bnick = self.arg[0]
            self.send("NICK %s" % self.bnick)
            
    def choose(self):
        if self.hasArgs:
            choices = self.longArg.split(",")
            i = 0
            if len(choices) > 1:
                for i in range(1, len(choices)):
                    choices[i] = choices[i].strip()
                self.msg("%s: %s" % (self.nick, random.choice(choices)), self.chan)
            else:
                self.msg("%s: Not enough arguments" % self.nick, self.chan)
        else:
            self.msg("%s: Not enough arguments." % self.nick, self.chan)
    
    def save(self):
        file = open("inventory.json", "w")    
        json.dump(self.inventory, file)
        file.close()
    
globals = gvars()
b = tacobot()
b.connect()

while True:
    b.command = ""
    b.longArg = ""
    b.longMsg = ""
    b.chan = ""
    b.arg = []
    b.nick = ""
    b.hasArgs = False
    
    try:
        line = b.bufferFile.readline().rstrip("\r\n")
    except UnicodeDecodeError:
        print("Can't use this line")
    else:
        if  line.find("PING") == 0:
           b.send(line.replace("PING", "PONG", 1))
        else:
            line = b.parse(line)
            if line["method"] == "PRIVMSG":
                message = line["arg"]
                #print(message)
                message = message.split(":", 1)
                b.chan = message[0]
                b.longMsg = message[1]
                message = message[1].split(" ", 1)
                b.command = message[0]
                b.nick = b.getNick(line["host"])    
               
                if b.command == "\x01ACTION":
                    mod1 = "*"
                    mod2 = ""
                    b.longMsg = b.longMsg.split(" ", 1)[1]
                else:
                    mod1 = "<"
                    mod2 = ">"

                text = "%s %s%s%s %s" % (str(datetime.datetime.now().time()).split(".")[0], mod1, b.nick, mod2, b.longMsg)

                b.log(b.chan, text)

                try:
                    print(text)
                except UnicodeEncodeError:
                    print("%s %s: <%s> Cannot decode message" % (str(datetime.datetime.now().time()).split(".")[0], b.chan, b.nick))

                if len(message) > 1:
                    b.longArg = message[1]
                    b.arg = b.longArg.split(" ")
                    b.hasArgs = True
                else:
                    hasArgs = False
                if len(b.command) > 0:
                    if b.command[0] == ";":
                        b.command = b.command.lstrip(";")
                        if b.command.lower() in b.commands.keys():
                            b.commands[b.command.lower()]()
                    
                    elif b.command.lower().rstrip(":") == b.bnick.lower() and b.hasArgs:
                        if b.arg[0].lower() in b.commands.keys():
                            if len(b.arg) == 1:
                                b.hasArgs = False
                                b.commands[b.arg[0].lower()]()
                            else:
                                b.command = b.arg[0]
                                b.longArg = b.longArg.split(" ", 1)[1]
                                b.hasArgs = True
                                b.arg.pop(0)
                                b.commands[b.command.lower()]()
                        else:
                            b.send("NOTICE %s :Not a command" % b.nick)
                    elif b.longMsg.lower().find("saturation") == 0:
                        b.msg(b.longMsg.lower().replace("saturation", "value"), b.chan)
            
            elif line["method"] == "001":
                b.send("JOIN :#tacobot")
                b.send("JOIN #programming")
                b.send("PRIVMSG NickServ :identify %s" % b.pwd)
                
            elif line["method"] == "005" and line["arg"].find("PREFIX") != -1:
                args = line["arg"].split()
                for i in range(1, len(args)):
                    if args[i].find("PREFIX") == 0:
                        globals.flags = args[i].split(")", 1)[1]
                        
            elif line["method"] == "NICK":
                chan = "global"
                text = "%s is now known as %s" % ((b.getNick(line["host"]), line["arg"].split(":", 1)[1]))
                b.log(chan, text)
                print(text)

            elif line["method"] == "INVITE":
                b.send("JOIN %s" % line["arg"].split(":", 1)[1])
                      
            else:
                print("%s %s" % (line["method"], line["arg"].replace(" :", ": ", 1)))                
           #
