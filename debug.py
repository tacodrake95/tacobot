class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "chansay"   : self.chanSay,
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def chanSay(self):
        if self.b.isMaster(self.b.nick):
            self.b.msg(self.b.longArg.split(" ", 1)[1], self.b.arg[0])
    
