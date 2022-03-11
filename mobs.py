import actions, actors, rsignals, tiles

class Mob(tiles.Occupant, actors.Actor):
    displayChar = "?"
    displayFG = (255, 0, 0)
    displayPriorityID = 0
    displayName = "unknown mob"

    health = 10

class Enemy(Mob):
    displayChar = "m"
    displayFG = (255, 0, 0)
    displayPriorityID = 1

    displayName = "unknown enemy"

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
        movTiles = [tile for tile in self.mob.tile.adjacentTiles() if self.mob.canOccupy(tile) ]

        if len(movTiles) > 0:
            return actions.ShiftStep(self.mob, self.roller.choice(movTiles))
        else:
            return actions.Wait(self.mob)
