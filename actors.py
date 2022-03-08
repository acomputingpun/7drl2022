class Actor():
    timeslots = 1

    def __init__(self):
        self.curAction = None

    def tryRequestAction(self):
        raise Exception

    def hasTimeslots(self):
        return self.timeslots > 0
    def refreshTimeslots(self):
        self.timeslots = 1
    def aConsumeTimeslot(self):
        self.timeslots = max(self.timeslots - 1, 0)


    def aTakeDamage(self, damage, interf):
        interf.activeWindow.afxDamageNumber(self, damage)
        if damage >= self.health:
            self.aDie()
    def aShiftStep(self, destTile, interf):
        interf.activeWindow.afxShiftStep(self, destTile)
        self.setTile(destTile)
        self.aConsumeTimeslot()
    def aWait(self, interf):
        self.aConsumeTimeslot()
