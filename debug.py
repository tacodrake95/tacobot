class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "nick"      : self.nickChange
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def nickChange(self):
        if self.b.isMaster(self.b.nick) and self.b.hasArgs:
            self.b.bnick = self.b.arg[0]
            self.b.send("NICK %s" % self.b.bnick)
