class main():
    def __init__(self, b):
        self.commands = {
                        "ding": self.dong
                        }
        self.b = b
        self.b.commands.update(self.commands)

    def unload(self):
        for key in self.commands:
            del self.b.commands[key]
        return True

    def dong(self):
        self.b.msg("dong\007", self.b.chan)
