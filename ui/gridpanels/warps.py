import vecs, dirconst
import actions, attacks
from .. import warps
from . import cursors, base

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
            if self.hero.canOccupy(destTile):
                self.trySubmitAction( actions.ShiftStep(self.hero, destTile ))
            else:
                if destTile is None:
                    self.interf.activeWindow.afxPostMessage( "Movement error: invalid destination." )
                elif destTile.occupant is not None:
                    self.interf.activeWindow.afxPostMessage( "Movement error: destination occupied." )
                else:
                    self.interf.activeWindow.afxPostMessage( "Movement error: invalid destination." )

    def warpOtherKey(self, key):
        if key == 113: # q
            self.interf.activeWindow.debug_postMessage()
        elif key == 119: # w
            self.trySubmitAction(actions.TakeDamage(self.hero, 3) )
        elif key == 101: # e
            self.interf.activeWindow.debug_afxZone()
        elif key == 114: # r
            pass
        elif key == 97: # a
            pass
        elif key == 115: #s
            pass
        elif key == 100: #d
            pass
        elif key == 102: #f
            self.transfer(AttackWarp(self.interf, attacks.StubBullet()))
        elif key == 120: # x
            self.transfer(ExamineWarp(self.interf))
        else:
            print ("Key was", key)

class CursorWarp(GameWindowWarp):
    def onTransferFrom(self, other):
        self.window.gridPanel.children.append(self.cursorFlyer)
    def onTransferTo(self, other):
        self.window.gridPanel.children.remove(self.cursorFlyer)

    def warpArrowKey(self, vec, shift = False):
        if self.cursorFlyer.shift(vec):
            self.refreshCursorData()
    def warpCancelKey(self):
        self.transfer(self.window.requestActionWarp(self.interf))
    def warpTabKey(self):
        if self.cursorFlyer.jumpToNextTab():
            self.refreshCursorData()

    def cursorTile(self):
        return self.cursorFlyer.tile
    def refreshCursorData(self):
        pass

    def getTabPoses(self):
        return []

class ExamineWarp(CursorWarp):
    def __init__(self, interf):
        super().__init__(interf)
        self.cursorFlyer = cursors.ExamineCursor(self.window.gridPanel, self.state.hero.xyPos, [k for k in self.getTabPoses()] )

    def getTabPoses(self):
        for tile in self.state.grid.allTiles():
            if len([*tile.listContents()]) > 0:
                yield tile.xyPos

    def warpSelectKey(self):
        pass
    def refreshCursorData(self):
        for item in self.cursorTile.listContents():
            pass

class AttackWarp(CursorWarp):
    def __init__(self, interf, atkProfile):
        super().__init__(interf)
        self.atkProfile = atkProfile

        self.cursorFlyer = cursors.SelectAttackCursor(self.window.gridPanel, self.state.hero.xyPos, [k for k in self.getTabPoses()] )
        self.zoneOverlay = base.AnimatedZoneOverlay( self.window.gridPanel, atkProfile.inRangePosesFrom(self.state.hero.xyPos), self.state.hero.xyPos )
        self.zoneOverlay.register(interf)

    def getTabPoses(self):
        for tile in self.atkProfile.inRangeTilesFrom(self.state.hero.tile):
            if not (tile.occupant is None or tile.occupant is self.state.hero):
                yield tile.xyPos

    def onTransferFrom(self, other):
        self.window.gridPanel.children.append(self.cursorFlyer)
        self.window.gridPanel.children.append(self.zoneOverlay)
    def onTransferTo(self, other):
        self.window.gridPanel.children.remove(self.cursorFlyer)
        self.window.gridPanel.children.remove(self.zoneOverlay)

    def warpSelectKey(self):
        print ("Select key was pressed over tile", self.cursorTile(), "w/occ", self.cursorMob, "and path", self.cursorFlyer.xyPathNodes)
        if self.cursorMob() is not None:
            self.trySubmitAction(actions.PathAttack(self.hero, None, self.cursorMob(), self.cursorFlyer.pathTiles()) )

    def cursorMob(self):
        return self.cursorTile().occupant