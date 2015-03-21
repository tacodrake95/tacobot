class main():
    def __init__(self, b):
        self.commands = {
                        "add": self.addItem
                        }
        self.b = b
        self.b.commands.update(self.commands)

    def unload(self):
        for key in self.commands:
            del self.b.commands[key]
        return True

    def addItem(self):
        #self.b.msg("Placeholder text to save this command's place", self.b.chan)
        if self.b.isMaster(self.b.nick):
            if self.b.isANum(self.b.arg[0]):
                item = self.b.longArg.split(" ", 1)[1]
                amt = int(self.b.arg[0])
            else:
                item = self.b.longArg
                amt = 1
            self.b.inventory[self.b.nick.lower()][item.lstrip().rstrip()] = {"amount": amt}
            self.b.msg("You have created %s %s" % (amt, item.lstrip().rstrip()), self.b.chan)
            self.b.save()
