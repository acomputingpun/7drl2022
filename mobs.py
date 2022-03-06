import actions, rsignals

class Mob(actions.Actor):
    def __init__(self):
        super().__init__()
        self.brain = WaitBrain(self)

    def tryRequestAction(self):
        self.bSubmitAction(self.brain.getNextAction())
        return rsignals.Advance()

    def bSubmitAction(self, action):
        self._submitAction(action)

class Brain():
    def __init__(self, mob):
        self.mob = mob

class WaitBrain(Brain):
    def getNextAction(self):
        return Wait(self.mob)

class RandomWalkBrain(Brain):
    """todo: To implement"""
