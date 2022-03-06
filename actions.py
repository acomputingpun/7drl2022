import rsignals

class Actor():
    def __init__(self):
        self.curAction = None

    def tryAdvance(self):
        if self.curAction is None:
            return self.tryRequestAction()
        else:
            return self.curAction.tryAdvance()

    def tryRequestAction(self):
        raise Exception

    def _submitAction(self, action):
        if self.curAction is not None:
            raise Exception
        elif action.actor is not self:
            raise Exception
        else:
            self.curAction = action

class Action():
    def __init__(self, actor):
        self.actor = actor
        self._started = False
        self._completed = False

    def tryAdvance(self):
        if self._completed:
            return rsignals.ActionCompleted(self)
        elif self._started:
            return self.tryInnerAdvance()
        else:
            return rsignals.ActionNotStarted(self)

    def tryInnerAdvance(self):
        raise NotImplementedError

    def rStart(self):
        if self._started:
            raise Exception
        self._started = True

    def rCleanup(self)
        if not self._completed:
            raise Exception
        self.actor.curAction = None
        "todo: remove an activation from the actor"

class Wait(Action):
    def __init__(self, actor):
        super(actor)

    def tryInnerAdvance(self):
        self._completed = True
        return rsignals.Advance()

class ShiftStep(Action):
    def __init__(self, actor, dest):
        super(actor)
        self.destTile = destTile

    def tryInnerAdvance(self):
        self.actor.setTile(self.destTile)
        self._completed = True
        return rsignals.Advance()

class BumpAttack(Action):
    def __init__(sefl, actor, target):
        super(actor)
        self.target = target

    def tryInnerAdvance(self):
        "todo: work out the exact behaviour of BumpAttack."
        return rsignals.Advance()

class PathAttack(Action):
    def __init__(self, actor, target, path):
        super(actor)
        self.target = target
        self.path = path

    def tryInnerAdvance(self):
        "todo: work out the exact behaviour of BumpAttack."
        return rsignals.Advance()