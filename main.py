class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {}
        
        self.b.commands.update(self.commands)

    def unload (self):
        for key in self.commands:
            del self.b.commands[key]
        return True
