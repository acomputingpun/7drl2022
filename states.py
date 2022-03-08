import zones, heros, actions, mobs, pseudo

class State():
    def __init__(self):
        self.curAction = None 
        self.roller = pseudo.Roller(1)

        self.hero = heros.Hero()
        self.activeZone = zones.BasicZone()
        self.stubSetup()

    def stubSetup(self):
        self.hero = heros.Hero()

        self.activeZone.addActor(self.hero)
        self.hero.setTile(self.activeZone.grid.lookup( (4, 4) ))

        bMob = mobs.Mob(self.roller)
        bMob.setTile(self.activeZone.grid.lookup((2, 2)))
        self.activeZone.addActor(bMob)

    def tryAdvance(self, interf):
        if self.curAction is None:
            nextAction = self.tryRequestNextAction(interf)
            if nextAction is not None:
                self.curAction = nextAction
        else:
            self.curAction.tryAdvance(interf)
            self.curAction = None

    def tryRequestNextAction(self, interf):
        nextActor = self.activeZone.getCurActor()
        if nextActor is not None:
            return nextActor.tryRequestAction(interf)