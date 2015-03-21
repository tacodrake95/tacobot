class main():
    def __init__(self, b):
        self.commands = {
                        "test": self.testCommand,
                        "othertest": self.otherTest,
                        "lol": self.lol,
                        "ding": self.ding
                        }
        self.b = b
        self.b.commands.update(self.commands)

    def unload(self):
        for key in self.commands:
            del self.b.commands[key]
        return True

    def testCommand(self):
        self.b.msg("Dynamical jercos", self.b.chan)

    def otherTest(self):
        if self.b.hasArgs:
            self.b.msg("You just said %s" % self.b.longArg, self.b.chan)

    def lol(self):
        self.b.action("laughs", self.b.chan)

    def ding(self):
        if self.b.hasArgs:
            self.b.msg("dong %s" % self.b.longArg.lower(), self.b.chan)
        else:
            self.b.msg("dong", self.b.chan)
