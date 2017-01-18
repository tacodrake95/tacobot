class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "action"    : self.do
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True
    
    def do(self):
        if self.b.hasArgs:
            self.b.action(self.b.longArg, self.b.chan)
