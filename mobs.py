import actions, actors, rsignals, tiles

class Mob(tiles.Occupant, actors.Actor):
    drawChar = "m"

    def __init__(self, roller):
        super().__init__()
        self.roller = roller
        self.brain = RandomWalkBrain(self)

    def tryRequestAction(self, interf):
        return self.brain.getNextAction()

class Brain():
    def __init__(self, mob):
        self.mob = mob

    @property
    def roller(self):
        return self.mob.roller

class WaitBrain(Brain):
    def getNextAction(self):
        return actions.Wait(self.mob)

class RandomWalkBrain(Brain):
    def getNextAction(self):
        # get adjacent tiles
        adjTiles = self.mob.tile.adjacentTiles()

        if len(adjTiles) > 0:
            return actions.ShiftStep(self.mob, self.roller.choice(adjTiles))
        else:
            return actions.Wait(self.mob)
