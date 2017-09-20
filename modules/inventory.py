class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {"give" : self.give,
                         "inventory" : self.inv,
                         "save" : self.save}
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def save(self):
        file = open("inventory.json", "w")    
        json.dump(self.inventory, file)
        file.close()

    def give(self):
        
        fromNick = self.nick.lower()
        if self.hasArgs:
            toNick = self.arg[0].lower()

        if not (fromNick in self.inventory.keys()):
            self.inventory[fromNick] = {"dong": {"amount": 1}}
            self.save()
            
        if self.hasArgs:
            if True:#self.isInChannel(toNick, self.chan):
                if not (toNick in self.inventory.keys()):
                    self.inventory[toNick] = {"dong": {"amount": 1}}
                    self.save()
                    
                if len(self.arg) >= 2:
                    if self.isANum(self.arg[1]):
                        if len(self.arg) >= 3:
                            item = self.longArg.split(" ", 2)[2]
                            amount = int(self.arg[1])
                        else:
                            amount = 0
                    else:
                        if self.arg[1].lower() == "a" or self.arg[1].lower() == "an":
                            item = self.longArg.split(" ", 2)[2]
                        else:
                            item = self.longArg.split(" ", 1)[1]
                        amount = 1

                    if amount > 0:
                        if item in self.inventory[fromNick].keys():
                            if self.inventory[fromNick][item]["amount"] >= amount:
                                self.msg("%s: you have given %s %s %s." % (self.nick, self.arg[0], amount, item), self.chan)
                                self.inventory[fromNick][item]["amount"] -= amount
                                if item in self.inventory[toNick].keys():
                                    self.inventory[toNick][item]["amount"] += amount
                                else:
                                    self.inventory[toNick][item]= {"amount": amount}
                                self.save()
                            else:
                                self.msg("%s: You don't have enough %s" %(fromNick, item), self.chan)
                        else:
                            self.msg("%s: You don't have any %s." % (fromNick, item), self.chan)
                    else:
                        self.msg("%s: Format incorrect or invalid number, try again." % fromNick, self.chan)
                else:
                    self.msg("%s: Not enough arguments." % fromNick, self.chan)
            else:
                self.msg("%s: %s is not in the channel." % (fromNick, toNick), self.chan)
