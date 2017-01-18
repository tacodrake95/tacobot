class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "part"      : self.part,
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def part(self):
        if self.b.isMaster(self.b.nick):
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
