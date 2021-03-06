import vecs, dirconst, math
from . import warps, windows

from .gridpanels import base as gridpanels
from .msgpanels import base as msgpanels
from .sidepanels import base as sidepanels

class GameWindow(windows.Window):
    def __init__(self, interf):
        super().__init__(interf)

        self.gridPanel = gridpanels.GridPanel(self)
        self.msgPanel = msgpanels.MessagePanel(self)
        self.sidePanel = sidepanels.SidePanel(self)

        self.children = [self.gridPanel, self.msgPanel, self.sidePanel]

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        "todo: draw terminaly background"

    def debug_postMessage(self):
        self.msgPanel.postPlaintext("Here's a message, right here.")

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
    def afxMessageInterrupt(self):
        self.interf.activeWarp.transfer(InputBlockedWarp(self.interf))
    def afxPostMessage(self, message):
        self.msgPanel.postPlaintext(message)

    def requestActionWarp(self, interf):
        return self.gridPanel.requestActionWarp(interf)

class AnimaBlockedWarp(warps.AnimaBlockedWarp):
    def warpArrowKey(self, vec, shift = False):
        print ("atw - arrow key was", vec)
    def warpOtherKey(self, key):
        print ("atw - key was", key)

class InputBlockedWarp(warps.AnyKeyWarp):
    def onTransferFrom(self, other):
        self.interruptedWarp = other
    def warpKeydown(self, key, shift = False):
        self.transfer(self.interruptedWarp)