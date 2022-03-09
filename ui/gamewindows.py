import vecs, dirconst, math
from . import warps, windows

from .gridpanels import base as gridpanels
from .gridpanels import warps as gridwarps

class GameWindow(windows.Window):
    def __init__(self, interf):
        super().__init__(interf)

        self.gridPanel = gridpanels.GridPanel(self)
        self.msgPanel = MessagePanel(self)
        self.sidePanel = SidePanel(self)

        self.children = [self.gridPanel, self.msgPanel, self.sidePanel]

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        ren.drawText( (0,0), "hello world" )

    def afxShiftStep(self, mob, destTile):
        self.gridPanel.afxShiftStep(mob, destTile)
        self.interf.capture(AnimaBlockedWarp(self.interf))
    def afxDamageNumber(self, mob, damage):
        self.gridPanel.afxDamageNumber(mob, damage)
        self.interf.capture(AnimaBlockedWarp(self.interf))
    def afxPathAttack(self, mob, atkProfile, target, path):
        self.gridPanel.afxPathAttack(mob, atkProfile, target, path)
        self.interf.capture(AnimaBlockedWarp(self.interf))

    def afxAnimaBlock(self):
        self.interf.capture(AnimaBlockedWarp(self.interf))

    def requestActionWarp(self, interf):
        return gridwarps.RequestActionWarp(interf)

class AnimaBlockedWarp(warps.AnimaBlockedWarp):
    def warpArrowKey(self, vec, shift = False):
        print ("atw - arrow key was", vec)
    def warpOtherKey(self, key):
        print ("atw - key was", key)

from . import scions, animas

class SidePanel(scions.Panel):
    xyAnchor = (45, 0)
    _panelSize = vecs.Vec2(30, 50)

    def __init__(self, parent):
        super().__init__(parent)

    def drawOutline(self, ren):
        super().drawOutline(ren)

        for y in range(self.panelSize.y):
            ren.drawChar((0, y), "|" )

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        ren.drawText( (0, 0), "sidepanel")

class MessagePanel(scions.Panel):
    xyAnchor = (0, 0)
    _panelSize = vecs.Vec2(46, 5)

    def drawContents(self, ren):
        ren.drawText( (0, 0), "messagepanel")