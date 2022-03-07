import rsignals

class Actor():
    def __init__(self):
        self.curAction = None

    def tryRequestAction(self):
        raise Exception

class Action():
    def __init__(self, actor):
        self.actor = actor
        self._started = False
        self._completed = False

    def tryAdvance(self):
        if self._completed:
            return rsignals.ActionCompleted(self)
        elif self._started:
            return rsignals.ActionInProgress(self)
        else:
            return rsignals.ActionNotStarted(self)

    def rStart(self):
        if self._started:
            raise Exception
        self._started = True

    def rExecute(self):
        if not self._started:
            raise Exception
        elif self._completed:
            raise Exception
        self._execute()
        self._completed = True

    def _execute(self):
        raise NotImplementedError(0)

class Wait(Action):
    def __init__(self, actor):
        super().__init__(actor)

    def tryInnerAdvance(self):
        self._completed = True
        return rsignals.Advance()

class ShiftStep(Action):
    def __init__(self, actor, destTile):
        super().__init__(actor)
        self.destTile = destTile

    def _execute(self):
        self.actor.setTile(self.destTile)

class BumpAttack(Action):
    def __init__(sefl, actor, target):
        super().__init__(actor)
        self.target = target

    def _execute(self):
        "todo: work out the exact behaviour of BumpAttack."
        return rsignals.Advance()

class PathAttack(Action):
    def __init__(self, actor, target, path):
        super().__init__(actor)
        self.target = target
        self.path = path

    def _execute(self):
        "todo: work out the exact behaviour of BumpAttack."
        return rsignals.Advance()