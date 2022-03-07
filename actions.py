import rsignals

class Actor():
    def __init__(self):
        self.curAction = None

    def tryRequestAction(self):
        raise Exception

class BranchAction():
    def __init__(self, actor):
        self._subActions = []
        self._started = False
        self._finished = False

        self.actor = actor

    def tryAdvance(self, interf):
        if not self._started:
            self._started = True
            self._start(interf)
            raise rsignals.ActionStart(self)

        while len(self._subActions) > 0:
            if self._subActions[0]._finished:
                self._subActions = self._subActions[1:]
            else:
                self._subActions[0].tryAdvance()

        if not self._finished:
            self._finish(interf)
            self._finished = True

    def noSubActions(self):
        return rsignals.ActionCompleted(self)

    def _start(self, interf):
        raise NotImplementedError()
    def _finish(self, interf):
        raise NotImplementedError()

class Wait(BranchAction):
    def __init__(self, parent, actor):
        super().__init__(parent, actor)

    def _start(self, interf):
        pass
    def _finish(self, interf):
        print("mob {} waits".format(self.actor))

class ShiftStep(BranchAction):
    def __init__(self, actor, destTile):
        super().__init__(actor)
        self.destTile = destTile

    def _start(self, interf):
        pass
    def _finish(self, interf):
        self.actor.setTile(self.destTile)
        print("mob {} moves to {}".format(self.actor, self.destTile))

class BumpAttack(BranchAction):
    def __init__(sefl, actor, target):
        super().__init__(actor)
        self.target = target

    def _finish(self, interf):
        "todo: work out the exact behaviour of BumpAttack."

class PathAttack(BranchAction):
    def __init__(self, actor, target, path):
        super().__init__(actor)
        self.target = target
        self.path = path

    def _finish(self, interf):
        "todo: work out the exact behaviour of BumpAttack."