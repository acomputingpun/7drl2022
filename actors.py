class Actor():
    timeslots = 1
    health = 10

    def __init__(self):
        self.curAction = None

    def tryRequestAction(self):
        raise Exception

    def hasTimeslots(self):
        return self.timeslots > 0
    def refreshTimeslots(self):
        self.timeslots = 1
    def actConsumeTimeslot(self):
        self.timeslots = max(self.timeslots - 1, 0)


    def actTakeDamage(self, damage, interf):
        interf.activeWindow.afxDamageNumber(self, damage)
        if damage >= self.health:
            self.aDie()
    def actShiftStep(self, destTile, interf):
        interf.activeWindow.afxShiftStep(self, destTile)
        self.setTile(destTile)
        self.actConsumeTimeslot()
    def actWait(self, interf):
        self.actConsumeTimeslot()

    def actBumpAttack(self, atkProfile, target, interf):
        interf.activeWindow.afxPathAttack(self, atkProfile, target)

    def actPathAttack(self, atkProfile, target, path, interf):
        interf.activeWindow.afxPathAttack(self, atkProfile, target, path)
        "todo: handle the actual effects of the attack here"
        target.actTakeDamage(2, interf)