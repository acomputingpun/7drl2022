import vecs, dirconst
from . import warps, gridpanels
import actions

class GameWindowWarp(warps.Warp):
    @property
    def hero(self):
        return self.interf.state.hero

    def trySubmitAction(self, action):
        self.interf.release(action)

class RequestActionWarp(GameWindowWarp):
    def warpArrowKey(self, vec, shift = False):
        if vec == dirconst.IN_PLACE:
            self.trySubmitAction( actions.Wait(self.hero) )
        elif vec in dirconst.CARDINALS:
            destTile = self.hero.tile.relTile(vec)
            self.trySubmitAction( actions.ShiftStep(self.hero, destTile ))

    def warpOtherKey(self, key):
        if key == 113: # q
            self.interf.activeWindow.debug_addLBF()
        elif key == 119: # w
            self.trySubmitAction(actions.TakeDamage(self.hero, 3) )
        elif key == 101: # e
            pass
        elif key == 114: # r
            pass
        elif key == 97: # a
            pass
        elif key == 115: #s
            pass
        elif key == 100: #d
            pass
        elif key == 102: #f
            self.transfer(AttackWarp(self.interf, None))
        elif key == 120: # x
            self.transfer(ExamineWarp(self.interf))
        elif key == 9: # tab
            pass
        else:
            print ("Key was", key)


class CursorWarp(GameWindowWarp):
    def onTransferFrom(self, other):
        self.window.gridPanel.children.append(self.cursorFlyer)
    def onTransferTo(self, other):
        self.window.gridPanel.children.remove(self.cursorFlyer)

    def warpArrowKey(self, vec, shift = False):
        self.cursorFlyer.shift(vec)
    def warpCancelKey(self):
        self.transfer(self.window.requestActionWarp(self.interf))

    def cursorTile(self):
        return self.cursorFlyer.tile

class ExamineWarp(CursorWarp):
    def __init__(self, interf):
        super().__init__(interf)
        self.cursorFlyer = gridpanels.ExamineCursor(self.window.gridPanel, self.state.hero.xyPos )

    def warpSelectKey(self):
        pass

class AttackWarp(CursorWarp):
    def __init__(self, interf, atkProfile):
        super().__init__(interf)
        self.cursorFlyer = gridpanels.SelectAttackCursor(self.window.gridPanel, self.state.hero.xyPos )

    def warpSelectKey(self):
        print ("Select key was pressed over tile", self.cursorTile(), "w/occ", self.cursorMob, "and path", self.cursorFlyer.xyPathNodes)
        if self.cursorMob() is not None:
            self.trySubmitAction(actions.PathAttack(self.hero, None, self.cursorMob, self.cursorFlyer.pathTiles()) )

    def cursorMob(self):
        return self.cursorTile().occupant