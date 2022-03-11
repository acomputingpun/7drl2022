import grids, rsignals
import vecs, dirconst

class TurnScheduler():
    def __init__(self):
        self.actors = []

    def curActor(self):
        if len(self.actors) > 0:
            return self.actors[0]
        else:
            return None

    def refresh(self):
        if len(self.actors) > 0:
            while not self.actors[0].hasTimeslots():
                self.actors[0].refreshTimeslots()
                self.actors = self.actors[1:] + self.actors[:1]

class Zone():
    def __init__(self):
        self.grid = grids.Grid( vecs.Vec2(11, 11) )
        self.turnScheduler = TurnScheduler()

        self.fillGrid()

    def tryAdvance(self):
        self.turnScheduler.refresh()

        if self.curActor is None:
            return rsignals.Intercession(self, "no existing actor")
        else:
            return self.curActor.tryRequestAction()

    def getCurActor(self):
        self.turnScheduler.refresh()
        return self.turnScheduler.curActor()

    def addActor(self, actor):
        self.turnScheduler.actors.append(actor)

    def allActors(self):
        return self.turnScheduler.actors[:]
    def sortedActors(self):
        return sorted( self.allActors(), key= lambda actor: actor.displayPriorityID )

    def fillGrid(self):
        raise NotImplementedError

import terrains
class BasicZone(Zone):
    def fillGrid(self):
        "todo: Populate the grid with various tiles, mobs, et cetera.  For now we just fill it with a bunch of generic tiles"
        for tile in self.grid.allTiles():
            tile.terrain = terrains.Floor(tile)