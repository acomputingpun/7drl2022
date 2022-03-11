import vecs, xchars
from .. import scions

class SidePanel(scions.Panel):
    xyAnchor = (45, 0)
    _panelSize = vecs.Vec2(30, 52)

    def __init__(self, parent):
        super().__init__(parent)

    def drawOutline(self, ren):
        ren.drawRect( (0,0), self.panelSize, " ", fg=(0, 255, 0), bg = (20, 20, 20) )
        for y in range(self.panelSize.y):
            ren.drawXChar((0, y), xchars.NS_LINE )

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        yDraw = 0
        yDraw = self.drawPlayerData(ren, yDraw)
        yDraw += 1
        yDraw = self.drawVisionData(ren, yDraw)
        yDraw += 1
        yDraw = self.drawProgramData(ren, yDraw)
        yDraw += 1
        yDraw = self.drawInventory(ren, yDraw)

    def drawPlayerData(self, ren, yDraw):
        ren.drawText( (1, yDraw), "CORE DATA:" )
        yDraw += 1
        return yDraw

    def drawVisionData(self, ren, yDraw):
        ren.drawText( (1, yDraw), "LOCAL NETWORK:")
        yDraw += 1

        alreadySeen = set()
        actors = self.interf.state.activeZone.sortedActors()
        for mob in actors:
            if mob not in alreadySeen:
                alreadySeen.add(mob)
                ren.drawChar( (2, yDraw), mob.displayChar, mob.displayFG )
                ren.drawText( (4, yDraw), mob.displayName )
                yDraw += 1

        return yDraw

    def drawInventory(self, ren, yDraw):
        ren.drawText( (1, yDraw), "DATA STORAGE:" )
        yDraw += 1
        return yDraw

    def drawProgramData(self, ren, yDraw):
        ren.drawText( (1, yDraw), "RUNNING PROCESSES:" )
        yDraw += 1
        return yDraw