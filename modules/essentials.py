import sys

class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "quit" : self.reset,
                        "reset" : self.reset,
                        "chansay" : self.chanSay,
                        "part" : self.part,
                        "join" : self.join,
                        "nick" : self.nickChange,
                        "action" : self.do
                        }
        
        self.b.commands.update(self.commands)
    
    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True
    
    def raw(self):
        if self.b.isMaster(self.b.nick):
           self.b.send(self.b.longArg)
    
    def ping(self):
        if self.b.hasArgs:
            self.b.msg("Pong %s" % self.b.longArg, self.b.chan)
        else:
            self.b.msg("Pong", self.b.chan)
    
    def reset(self):
        if self.b.isMaster(self.b.nick):
            self.b.send("QUIT :%s" % self.b.longArg)
            print("Quitting.")
            self.b.s.close()
            self.b.save()
            sys.exit()
    
    def chanSay(self):
        if self.b.isMaster(self.b.nick):
            self.b.msg(self.b.longArg.split(" ", 1)[1], self.b.arg[0])

    
    def part(self):
        if self.b.isMaster:
            if self.b.hasArgs:
                if len(self.b.arg) == 1:
                    if self.b.arg[0] == "":
                        args = self.b.chan
                    else:
                        args = self.b.arg[0]
                elif len(self.b.arg) >= 2:
                    lArg = self.b.longArg.split(" ", 1)[1]
                    args = "%s :%s" % (self.b.arg[0], lArg)
            else:
                args = self.b.chan

    def commands(self):
        self.send("NOTICE %s :Commands:" % self.nick)
        commands = ""
        for key in self.commands:
            commands = "%s %s" % (commands, key)
            
        commands = commands.strip().replace(" ", ", ")
        self.send("NOTICE %s :%s" % (self.nick, commands))

    def penis(self):
        if self.hasArgs:
            self.msg("dong %s" % self.longArg, self.chan)
        else:
            self.msg("dong", self.chan)

    def say(self):
        if self.hasArgs:
           self.msg(self.longArg, self.chan)
        else:
            self.msg("No args", self.chan)

    def choose(self):
        if self.hasArgs:
            choices = self.longArg.split(",")
            i = 0
            if len(choices) > 1:
                for i in range(1, len(choices)):
                    choices[i] = choices[i].strip()
                self.msg("%s: %s" % (self.nick, random.choice(choices)), self.chan)
