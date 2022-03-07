import zones, heros, actions, mobs

class State():
    def __init__(self):
        self.hero = heros.Hero()
        self.activeZone = zones.BasicZone()

        self.activeZone.addActor(self.hero)
        self.hero.setTile(self.activeZone.grid.lookup( (4, 4) ))

        bMob = mobs.Mob()
        bMob.setTile(self.activeZone.grid.lookup((2, 2)))
        self.activeZone.addActor(bMob)

        self._subActions = []

    def tryAdvance(self, interf):
        while True:
            if len(self._subActions) == 0:
                self.tryRequestNextAction(interf)
            elif self._subActions[0]._finished:
                self._subActions = self._subActions[1:]
            else:
                self._subActions[0].tryAdvance(interf)

    def tryRequestNextAction(self, interf):
        nextActor = self.hero
        nextActor.tryRequestAction()

    def rSubmitAction(self, action):
        self._subActions.append(action)