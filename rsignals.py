class Signal(Exception):
    sigCode = "SIGNAL"

    def __init__(self, msg = "?"):
        self.msg = msg

    def __str__(self):
        return self.sigCode + " " + self.msg

class Intercession(Signal):
    sigCode = "INTR"

    def __init__(self, blockingEntity, msg = "?"):
        super().__init__(msg)
        self.blockingEntity = blockingEntity

    def __str__(self):
        return self.sigCode + "|" + str(self.blockingEntity) + "|" + self.msg

class ActionStart(Intercession):
    sigCode = "IA_START"
class ActionInputRequired(Intercession):
    sigCode = "INP_ACTREQ"