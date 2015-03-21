class main():
    def __init__(self, b):
        self.newMasters = ["sammi", "Roman", "Ari", "nathan", "splashy"]
        self.b = b
        self.b.master.extend(self.newMasters)

    def unload(self):
        for key in self.newMasters:
            self.b.master.remove(key)
        return True
