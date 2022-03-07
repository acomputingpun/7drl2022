import zones, heros, actions, mobs

class State():
    def __init__(self):
        self.curAction = None 

        self.hero = heros.Hero()
        self.activeZone = zones.BasicZone()

        self.activeZone.addActor(self.hero)
        self.hero.setTile(self.activeZone.grid.lookup( (4, 4) ))

        bMob = mobs.Mob()
        bMob.setTile(self.activeZone.grid.lookup((2, 2)))
        self.activeZone.addActor(bMob)

    def tryAdvance(self, interf):
        if self.curAction is None:
            self.curAction = self.tryRequestNextAction(interf)
        else:
            self.curAction.tryAdvance(interf)
            self.curAction = None

    def tryRequestNextAction(self, interf):
        nextActor = self.hero
        return nextActor.tryRequestAction(interf)