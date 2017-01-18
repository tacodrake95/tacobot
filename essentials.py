class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "raw" : self.raw,
                        "ping" : self.ping,
                        "quit" : self.reset,
                        "reset" : self.reset,
                        "getcwd" : self.cwd,
                        "chansay" : self.chanSay,
                        "part" : self.part,
                        "join" : self.join,
                        "nick" : self.nickChange,
                        "action" : self.do,
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
    
            self.b.send("PART %s" % args)

    def join(self):
        if self.b.hasArgs and self.b.isMaster:
            self.b.send("JOIN %s" % self.b.arg[0])
    
    def nickChange(self):
        if self.b.isMaster(self.b.nick) and self.b.hasArgs:
            self.b.bnick = self.b.arg[0]
            self.b.send("NICK %s" % self.b.bnick)
    
    

