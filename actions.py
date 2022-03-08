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
        self.actor.actWait(interf)

class ShiftStep(Action):
    def __init__(self, actor, destTile):
        super().__init__(actor)
        self.destTile = destTile

    def _advance(self, interf):
        self.actor.actShiftStep(self.destTile, interf)

class TakeDamage(Action):
    def __init__(self, actor, damage):
        super().__init__(actor)
        self.damage = damage

    def _advance(self, interf):
        self.actor.actTakeDamage(self.damage, interf)

class BumpAttack(Action):
    def __init__(self, actor, atkProfile, target):
        super().__init__(actor)
        self.atkProfile = atkProfile
        self.target = target

    def _advance(self, interf):
        self.actor.actBumpAttack(self.atkData, self.target, interf)

class PathAttack(Action):
    def __init__(self, actor, atkProfile, target, path):
        super().__init__(actor)
        self.atkProfile = atkProfile
        self.target = target
        self.path = path

    def _advance(self, interf):
        self.actor.actPathAttack(self.atkProfile, self.target, self.path, interf)
