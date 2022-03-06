import zones

class State():
    def __init__(self):
        self.activeZone = zones.BasicZone()

    def tryAdvance(self):
        if self.activeZone is not None:
            return self.activeZone.tryAdvance()
        else:
            raise NotImplementedError()