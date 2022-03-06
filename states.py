class State():
    def __init__(self):
        self.activeZone = Zone()

    def advance(self, interf):
        self.requestAction(interf).advance(interf)

    def requestAction(self, interf):
        if self.activeZone is not None:
            return self.activeZone.requestAction(interf)
        else:
            raise NotImplementedError
#        return self.level.requestAction(interf)
 
class Zone():
    def __init__(self):
        pass

    def requestAction(self, interf):
        return Action()

class Action():
    def __init__(self):
        pass

    def advance(self, interf):
        raise NotImplementedError
