class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {"templatecommand" : self.templateCommand}
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def templateCommand (self):
        #Sends a message to a given channel
        #*****************************************************************
        #          MESSAGE                                    CHANNEL
        self.b.msg("This is a template for a tacobot module", self.b.chan)
