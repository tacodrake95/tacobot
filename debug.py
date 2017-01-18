class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "quit"      : self.reset,
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def reset(self):
        if self.b.isMaster(self.b.nick):
            self.b.send("QUIT :%s" % self.b.longArg)
            print("Quitting.")
            self.b.s.close()
            self.b.save()
            sys.exit()
    
