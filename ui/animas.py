import timing
from . import scions

class Anima():
    maxMS = 0
    blockingMS = 0

    def register(self, interf):
        self.timer = timing.SlaveTimer(interf.sysTimer)

        interf.livingAnimas.append(self)
        self.timer.unpause()
    def deregister(self, interf):
        interf.livingAnimas.remove(self)
    def fastUpkeep(self, interf):
        pass

    def MS(self):
        if self.maxMS == 0:
            return 0
        else:
            return min(self.timer.MS(), self.maxMS)
    def frac(self):
        if self.maxMS == 0:
            return 0
        else:
            return min(self.MS() / self.maxMS, 1)
    def isBlocking(self):
        return self.MS() < self.blockingMS

class Periodic():
    def __init__(self, interf, periodMS = 1000):
        self.timer = timing.SlaveTimer(interf.sysTimer)
        self.timer.unpause()
        self.periodMS = periodMS
    def MS(self):
        if self.periodMS == 0:
            return 0
        else:
            return self.timer.MS() % self.periodMS
    def frac(self):
        if self.periodMS == 0:
            return 0
        else:
            return self.MS() / self.periodMS
    def sawtoothFrac(self):
        return abs(self.frac() - 0.5)*2

    def reset(self):
        self.timer.reset()

class Flyer(Anima, scions.Scion):
    def fastUpkeep(self, interf):
        if self.frac() >= 1:
            self.deregister(interf)
            self.parent.children.remove(self)

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        pass