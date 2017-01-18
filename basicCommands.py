class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "raw" : self.raw,
                        "ping" : self.ping,
                        
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
