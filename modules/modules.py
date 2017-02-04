import sys

class main():
    
    def __init__(self, b):
        self.b = b
        
        self.commands = {
                        "unload" : self.unloadModule,
                        "reload" : self.reloadModule
                        }
        
        self.b.commands.update(self.commands)

    def unload (self):
        #Remove command references
        for key in self.commands:
            del self.b.commands[key]
        return True

    def unloadModule(self):
        if self.b.isMaster(self.b.nick) and self.b.hasArgs:
            modName = self.b.arg[0]
            if modName in self.b.modules:
                if not self.b.modules[modName].unload():
                    self.b.msg("It seems as though your unload procedure failed in this module. Ther may be residual goo from the module.", self.b.chan)
                    unloadFail = True
                else:
                    unloadFail = False
                del self.b.modules[modName]
                del sys.modules[modName]
                if not unloadFail:
                    self.b.msg("Module unloaded successfully.", self.b.chan)
            else:
                self.b.msg("I haven't loaded that stupid module yet, shitwad.", self.b.chan)
    
    def reloadModule(self):
        if self.b.isMaster(self.b.nick):
            self.unloadModule()
            self.b.loadModule()
