class main():
    def __init__(self, b):
        self.commands = {
                        "piss": self.waffle
                        }
        self.b = b
        self.b.commands.update(self.commands)

    def unload(self):
        for key in self.commands:
            del self.b.commands[key]
        return True

    def waffle(self):
        self.b.msg("\x0308waffle", self.b.chan)
