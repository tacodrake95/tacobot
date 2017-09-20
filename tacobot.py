# Copyright (c) 2016 Jake Drake
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import socket
import random
import sys
import time
import os
import string
import datetime
import ssl
import json
import importlib

import os.path

class tacobot:

    def __init__(self):
        if sys.platform == "win32":
            self.pathSep = "\\"
        else:
            self.pathSep = "/"

        os.chdir(os.path.abspath(sys.argv[0]).rsplit(self.pathSep, 1)[0])
        
        sys.path.append(os.getcwd())

        self.bnick = "tacobot"
        self.commands = {"load" : self.loadModule}
        self.host = "irc.0x00sec.org"
        self.port = 6667
        self.ident = "tacobot"
        self.name = "Taco Bell Bot"
        self.master = ["taco", "not_taco"]
        self.bufferFile = ""
        self.s = socket.socket( )
        #self.s = ssl.wrap_socket(self.s)
        self.modules = {}

        #init command vars
        self.command = ""
        self.longArg = ""
        self.longMsg = ""
        self.chan = ""
        self.arg = []
        self.nick = ""
        self.hasArgs = False

        self.pwd = ""#open("%s%spwd.dat" % (os.getcwd(), pathSep)).readline().rstrip("\n")

     
    def connect(self):
        self.s.connect((self.host, self.port))
        self.bufferFile = self.s.makefile()
        self.send("USER %s %s %s :%s" % (self.ident, self.host, self.bnick, self.name))
        self.send("NICK %s" % self.bnick)
 
    def parse(self, msg):
        splitmsg = msg.split(" ", 2)
        info = {"method": splitmsg[1], "host": splitmsg[0][1:], "arg": splitmsg[2].replace("\x07", "")}
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
        inLine = ""
        nicksLine = ""
        names = ""
        while (inLine.find("366") != 0):
            try:
                inLine = self.bufferFile.readline().rstrip("\r\n")
            except UnicodeDecodeError:
                inLine = "NOMETHOD nouser!nohost :nomsg"
            if inLine.find("PING") == 0:
                self.send(inLine.replace("PING", "PONG", 1))
                line = {"method" : "NOMETHOD"}
            elif inLine.find("353") == 0:
                line = self.parse(inLine)
                nicksLine += line["arg"]
            print(inLine)
        
        names = nicksLine.rsplit(":", 1)[1].strip().lower()
        names = ([i.lstrip(" %s" % globals.flags) for i in names.split()])
        return nick in names

    def getNick(self, host):
        return host.split("!", 1)[0]

    def action(self, msg, chan):
        self.send("PRIVMSG %s :\x01ACTION %s\x01" % (chan, msg))
        text = "%s *%s %s" % (str(datetime.datetime.now().time()).split(".")[0], self.bnick, msg)
        
    def getAuth(self, nick):
        """
        self.send("PRIVMSG NickServ ACC %s" % nick)
        line = {"method" : "NOMETHOD"}
        while line["method"] != "NOTICE":
            line = self.bufferFile.readline().rstrip("\r\n")
            if line.find("PING") == 0:
               self.send(line.replace("PING", "PONG", 1))
               line = {"method" : "NOMETHOD"}
            else:
                line = self.parse(line)
        """     
        #self.args = line["arg"].split()
        #print(line["arg"])
        #self.args[1].strip(":")
        return(nick in self.master) #and self.args[2]== "ACC" and self.args[3] == "3")

    def toggle(self, boolean):
        try:
            return not boolean
        except:
            print("Not a boolean")
            return boolean

    def msg(self, msg, chan):
        #self.send("PRIVMSG %s :\x0310%s" % (chan, msg))
        self.send("PRIVMSG %s :%s" % (chan, msg))
        text = "%s <%s> %s" % (str(datetime.datetime.now().time()).split(".")[0], self.bnick, msg)


    def send(self, msg):
        print(msg)
        self.s.sendall(bytes("%s\r\n" % msg, "UTF-8"))
    

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

    def loadModule(self):
        if self.isMaster(self.nick) and self.hasArgs:
            modName = self.arg[0]
            if os.path.isfile("%s%smodules%s%s.py" % (os.getcwd(), self.pathSep, self.pathSep, modName)):

                initFail = False
                try:
                    self.modules[modName] = importlib.import_module(".%ssmodules%s%s.py" % (self.pathSep, self.pathSep, modName)).main(self)
                    
                except AttributeError:
                    self.msg("You need a main class fuckface", self.chan)
                else:
                    if not hasattr(self.modules[modName], "__init__"):
                        self.msg("You forgot to \"def __init__(self)\" jerknips", self.chan)
                        initFail = True
                    if not hasattr(self.modules[modName], "unload"):
                        self.msg("What is this, OverCode? There isn't even an unload routine.", self.chan)
                        initFail = True
                    if initFail:
                        del self.modules[modName]
                        del sys.modules[modName]
                    else:
                        self.msg("Module loaded successfully", self.chan)
            else:
                self.msg("Check your fucking spelling, because I can't find that one. Dickface.", self.chan)
                self.msg("the attempted path is: %s" % ("%s%smodules%s%s.py" % (os.getcwd(), self.pathSep, self.pathSep, modName)), self.chan)


b=tacobot()
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
                    if b.command[0] == ";":                         #if leftmost char of "command" variable is ";"
                        b.command = b.command.lstrip(";")           #remove ";" from command string
                        cmdStr = b.command.lower()
                    #b.commands[b.command.lower()]()
                    
                    elif b.command.lower() == ".choose":
                        cmdStr = "choose"


                    elif b.command.lower().rstrip(":") == b.bnick.lower() and b.hasArgs:
                        if len(b.arg) == 1:
                            b.hasArgs = False
                            cmdStr = b.arg[0].lower()
                            #b.commands[b.arg[0].lower()]()
                        else:
                            b.command = b.arg[0]
                            b.longArg = b.longArg.split(" ", 1)[1]
                            b.hasArgs = True
                            b.arg.pop(0)
                            cmdStr = b.command.lower()
                            #b.commands[b.command.lower()]()
                    else:
                        cmdStr = ""
                    if cmdStr in b.commands.keys():
                        try:
                            b.commands[cmdStr]()
                        except Exception as e:
                            b.msg("%s: %s" % (e.__class__.__name__, e), b.chan)


                elif b.longMsg.lower().find("saturation") == 0:
                    b.msg(b.longMsg.lower().replace("saturation", "value"), b.chan)
            
            #elif line["method"] == "001":
                #b.send("JOIN :#tacobot")
                #b.send("JOIN #programming") 
                #b.send("PRIVMSG NickServ :identify %s" % b.pwd)
                
            elif line["method"] == "005" and line["arg"].find("PREFIX") != -1:
                args = line["arg"].split()
                for i in range(1, len(args)):
                    if args[i].find("PREFIX") == 0:
                        globals.flags = args[i].split(")", 1)[1]
                        
            elif line["method"] == "NICK":
                chan = "global"
                text = "%s is now known as %s" % ((b.getNick(line["host"]), line["arg"].split(":", 1)[1]))
                
                print(text)

            elif line["method"] == "INVITE":
                b.send("JOIN %s" % line["arg"].split(":", 1)[1])
                      
            else:
                print("%s %s" % (line["method"], line["arg"].replace(" :", ": ", 1)))                
           
