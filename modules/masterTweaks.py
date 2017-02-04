class main():
    def __init__(self, b):
        self.commands = {
                        "addmaster" : self.addMaster,
                        "delmaster" : self.delMaster
                        }
        self.b = b
        self.b.commands.update(self.commands)
        
    def unload(self):
        for key in self.commands:
            del self.b.commands[key]
        return True

    def delMaster(self):
        if self.b.isMaster(self.b.nick):
            try:
                self.b.master.remove(self.b.arg[0])
                self.b.msg("Removed %s from master list" % self.b.arg[0], self.b.chan)
            except:
                self.b.msg("%s is not in master list" % self.b.arg[0], self.b.chan)

    def addMaster(self):
        if self.b.isMaster(self.b.nick):
            if not self.b.arg[0] in self.b.master:
                self.b.master.append(self.b.arg[0])
                self.b.msg("Added %s to master list" % self.b.arg[0], self.b.chan)
            else:
                self.b.msg("%s is already in master list" % self.b.arg[0], self.b.chan)
