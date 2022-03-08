import rsignals

class Action():
    def __init__(self, actor):
        self.actor = actor
        self._finished = False

    def tryAdvance(self, interf):
        if not self._finished:
            self._advance(interf)
            self._finished = True

    def _advance(self, interf):
        raise NotImplementedError()

class Wait(Action):
    def __init__(self, actor):
        super().__init__(actor)

    def _advance(self, interf):
        self.actor.aWait(interf)

class ShiftStep(Action):
    def __init__(self, actor, destTile):
        super().__init__(actor)
        self.destTile = destTile

    def _advance(self, interf):
        self.actor.aShiftStep(self.destTile, interf)

class TakeDamage(Action):
    def __init__(self, actor, damage):
        super().__init__(actor)
        self.damage = damage

    def _advance(self, interf):
        self.actor.aTakeDamage(self.damage, interf)

class BumpAttack(Action):
    def __init__(self, actor, target):
        super().__init__(actor)
        self.target = target

    def _advance(self, interf):
        "todo: work out the exact behaviour of BumpAttack."

class PathAttack(Action):
    def __init__(self, actor, target, path):
        super().__init__(actor)
        self.target = target
        self.path = path

    def _advance(self, interf):
        "todo: work out the exact behaviour of BumpAttack."