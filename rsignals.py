class Signal():
    sigCode = "SIGNAL"

    def __init__(self, msg = "?"):
        self.msg = msg

    def __str__(self):
        return self.sigCode + " " + self.msg

class Advance(Signal):
    sigCode = "ADV"

class Intercession(Signal):
    sigCode = "INTR"

    def __init__(self, blockingEntity, msg = "?"):
        super().__init__(msg)
        self.blockingEntity = blockingEntity

    def __str__(self):
        return self.sigCode + "|" + str(self.blockingEntity) + "|" + self.msg

class ActionIntercession(Intercession):
    sigCode = "IACTION"

class ActionCompleted(ActionIntercession):
    sigCode = "IA_DONE"
class ActionNotStarted(ActionIntercession):
    sigCode = "IA_READY"
class ActionInProgress(ActionIntercession):
    sigCode = "IA_PROG"


class ActorIntercession(Intercession):
    sigCode = "IACTOR"
class ActionInputRequired(ActorIntercession):
    sigCode = "INP_ACTREQ"

class ZoneIntercession(Intercession):
    sigCode = "IZONE"
