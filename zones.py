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
            while "todo: self.actors[0] has an activation remaining!":
                "todo: refresh self.actors[0]'s activations"
                self.actors = self.actors[1:] + self.actors[:1]

class Zone():
    def __init__(self):
        self.grid = grids.Grid( vecs.Vec2(11, 11) )
        self.turnScheduler = TurnScheduler()

        self.fillGrid()

    def tryAdvance(self):
        self.turnScheduler.refresh()

        if self.curActor is None:
            return rsignals.Intercession(self)
        else:
            return self.curActor.tryAdvance()

    @property
    def curActor(self):
        return self.turnScheduler.curActor()

    def fillGrid(self):
        raise NotImplementedError

import terrains
class BasicZone(Zone):
    def fillGrid(self):
        "todo: Populate the grid with various tiles, mobs, et cetera.  For now we just fill it with a bunch of generic tiles"
        for tile in self.grid.allTiles():
            tile.terrain = terrains.Floor(tile)