import dirconst

class Warp():
    def __init__(self, interf):
        self.interf = interf

    def transfer(self, other):
        self.onTransferTo(other)
        self.interf._activeWarp = other
        other.onTransferFrom(self)
    def onTransferTo(self, other):
        pass
    def onTransferFrom(self, other):
        pass
    def fastUpkeep(self):
        pass

    @property
    def window(self):
        return self.interf.activeWindow
    @property
    def state(self):
        return self.interf.state

# True event handling
    def warpKeydown(self, key, shift=False):
        if key == 49: #1
            self.warpArrowKey(dirconst.SW, shift)
        elif key == 50: #2
            self.warpArrowKey(dirconst.S, shift)
        elif key == 51: #3
            self.warpArrowKey(dirconst.SE, shift)
        elif key == 52: #4
            self.warpArrowKey(dirconst.W, shift)
        elif key == 53: #5
            self.warpArrowKey(dirconst.IN_PLACE, shift)
        elif key == 54: #6
            self.warpArrowKey(dirconst.E, shift)
        elif key == 55: #7
            self.warpArrowKey(dirconst.NW, shift)
        elif key == 56: #8
            self.warpArrowKey(dirconst.N, shift)
        elif key == 57: #9
            self.warpArrowKey(dirconst.NE, shift)

        elif key == 1073741913: #num 1
            self.warpArrowKey(dirconst.SW, shift)
        elif key == 1073741914: #num 2
            self.warpArrowKey(dirconst.S, shift)
        elif key == 1073741915: #num 3
            self.warpArrowKey(dirconst.SE, shift)
        elif key == 1073741916: #num 4
            self.warpArrowKey(dirconst.W, shift)
        elif key == 1073741917: #num 5
            self.warpArrowKey(dirconst.IN_PLACE, shift)
        elif key == 1073741918: #num 6
            self.warpArrowKey(dirconst.E, shift)
        elif key == 1073741919: #num 7
            self.warpArrowKey(dirconst.NW, shift)
        elif key == 1073741920: #num 8
            self.warpArrowKey(dirconst.N, shift)
        elif key == 1073741921: #num 9
            self.warpArrowKey(dirconst.NE, shift)

        elif key == 1073741903: #right arrow
            self.warpArrowKey(dirconst.E, shift)
        elif key == 1073741904: #left arrow
            self.warpArrowKey(dirconst.W, shift)
        elif key == 1073741905: #down arrow
            self.warpArrowKey(dirconst.S, shift)
        elif key == 1073741906: #up arrow
            self.warpArrowKey(dirconst.N, shift)

        elif key == 9: # TAB
            self.warpTabKey()
        elif key == 27: # ESC
            self.warpCancelKey()
        elif key == 13: # ENTER
            self.warpSelectKey()
        elif key == 96: # `
            self.interf.forceQuit()

        else:
            self.warpOtherKey(key)

    def warpArrowKey(self, vec, shift = False):
        pass
    def warpSelectKey(self):
        pass
    def warpCancelKey(self):
        pass
    def warpTabKey(self):
        pass
    def warpOtherKey(self, key):
        print ("Key was", key)
    def warpQuit(self):
        raise SystemExit()


class GeneralDisplayWarp(Warp):
    def warpKeydown(self, key, shift = False):
        print ("Key was", key)

class AnyKeyWarp(Warp):
    def warpKeydown(self, key, shift = False):
        self.interf.release(None)

class AnimaBlockedWarp(Warp):
    def __init__(self, interf):
        super().__init__(interf)

    def onTransferFrom(self, other):
        pass
    def fastUpkeep(self):
        for anima in self.interf.livingAnimas:
            if anima.isBlocking():
                return
        else:
            self.interf.release(None)