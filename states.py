import zones, heros

class State():
    def __init__(self):
        self.hero = heros.Hero()
        self.activeZone = zones.BasicZone()

        self.activeZone.addActor(self.hero)
        self.hero.setTile(self.activeZone.grid.lookup( (4, 4) ))

        self.curAction = None

    def tryAdvance(self):
        if self.curAction is not None:
            return self.curAction.tryAdvance()
        elif self.activeZone is not None:
            return self.activeZone.tryAdvance()
        else:
            raise NotImplementedError()

    def rSubmitAction(self, action):
        self._submitAction(action)
    def rCleanupAction(self, action):
        if self.curAction is action:
            self.curAction = None
        else:
            raise Exception

    def _submitAction(self, action):
        if self.curAction is not None:
            raise Exception
        else:
            self.curAction = action
