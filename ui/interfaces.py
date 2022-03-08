import timing, vecs
from . import gamewindows

class Interface():
    _debugText = "debug"

    def __init__(self, intModule, state):
        self.state = state

        self.ren = intModule.Renderer(80, 60)
        self.eventHandler = intModule.EventHandler()

        self.sysTimer = timing.SlaveTimer(intModule.SystemTimer())
        self.activeWindow = gamewindows.GameWindow(self)
        self._activeWarp = None

        self.lastDrawMS = -1000
        self.livingAnimas = []

        self.sysTimer.unpause()

    def draw(self):
        if self.lastDrawMS + 25 < self.sysTimer.MS():
            self.lastDrawMS = self.sysTimer.MS()

            for anima in self.livingAnimas[:]:
                anima.fastUpkeep(self)

            self.ren.xyOffset = vecs.Vec2(0,0)
            self.ren.zLevel = 0
            self.activeWindow.draw(self.ren)

            self.ren.xyOffset = vecs.Vec2(0,0)
            self.ren.drawText( (0, 0), self._debugText)
            flushMS = self.sysTimer.MS()
            self.ren.flush()
            print ("draw took", self.sysTimer.MS() - self.lastDrawMS, "(flush", self.sysTimer.MS() - flushMS, ")")

        for anima in self.livingAnimas[:]:
            anima.fastUpkeep(self)

    def debugShow(self, text):
        self._debugText = str(text)

    @property
    def activeWarp(self):
        return self._activeWarp
    def capture(self, warp):
        if self.activeWarp is not None:
            raise Exception()
        else:
            self._activeWarp = warp

            self.activeWarp.onTransferFrom(None)
            self._releaseValue = None
            while self.activeWarp is not None:
                self.activeWarp.fastUpkeep()
                if self.activeWarp is not None:
                    self.eventHandler.warpEvents(self.activeWarp)
                self.draw()
            return self._releaseValue
    def release(self, value = None):
        self._releaseValue = value
        self.activeWarp.onTransferTo(None)
        self._activeWarp = None

    # utility
    def forceQuit(self):
        self.ren.forceQuit()
        raise Exception()

    # messaging
    def postMessage(self, message):
        self.activeWindow.msgPanel.addMessage(message)

    # warp transfers
    def warpRequestAction(self):
        return self.capture(self.activeWindow.requestActionWarp(self))

    def hasBlockingAnimas(self):
        return len(self.livingAnimas) > 0
    def showAnima(self, anima):
        anima.register(self)