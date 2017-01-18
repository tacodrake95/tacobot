class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "join"      : self.join,
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def join(self):
        if self.b.hasArgs and self.b.isMaster(self.b.nick):
            self.b.send("JOIN %s" % self.b.arg[0])
