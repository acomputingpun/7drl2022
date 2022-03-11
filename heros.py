import mobs

class Hero(mobs.Mob):
    displayChar = "@"
    displayFG = (0, 255, 255)
    displayName = "you"

    def tryRequestAction(self, interf):
        return interf.warpRequestAction()