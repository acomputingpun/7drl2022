import actions, rsignals, tiles

class Mob(tiles.Occupant, actions.Actor):
    drawChar = "m"

    def __init__(self):
        super().__init__()
        self.brain = WaitBrain(self)

    def tryRequestAction(self):
        return self.bSubmitAction(self.brain.getNextAction())

    def bSubmitAction(self, action):
        self.zone._submitAction(action)
        return self.action.tryAdvance()

class Brain():
    def __init__(self, mob):
        self.mob = mob

class WaitBrain(Brain):
    def getNextAction(self):
        return Wait(self.mob)

class RandomWalkBrain(Brain):
    """todo: To implement"""
