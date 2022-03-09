from .. import scions
from . import warps

class GridCursor(scions.Scion):
    fgDebug = (255, 255, 255)
    xyAnchor = (0, 0)

    def __init__(self, parent, startPos, tabPoses = []):
        super().__init__(parent)
        self.xyPos = self.startPos = startPos
        self.tabPoses = tabPoses[:]

    @property
    def grid(self):
        return self.parent.grid

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        xyDraw = self.parent.posToNWDraw(self.xyPos)

        ren.drawChar (xyDraw+(0, 0), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(2, 0), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(0, 2), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(2, 2), "*", fg = self.fgDebug)

    def shift(self, vec):
        xyNew = self.xyPos + vec
        if self.grid.rectContains(xyNew):
            self.xyPos = xyNew

    def jumpTo(self, xyNew):
        if self.grid.rectContains(xyNew):
            self.xyPos = xyNew

    def jumpToNextTab(self):
        if len(self.tabPoses) > 0:
            if self.xyPos == self.tabPoses[0]:
                self.tabPoses = self.tabPoses[1:] + self.tabPoses[:1]
            self.jumpTo(self.tabPoses[0])

    @property
    def tile(self):
        return self.grid.lookup(self.xyPos)

class TrailCursor(GridCursor):
    xyAnchor = (0, 0)

    def __init__(self, parent, startPos, tabPoses = []):
        super().__init__(parent, startPos, tabPoses)
        self.xyPathNodes = [self.startPos]
        self.pathDraws = []

    def shift(self, vec):
        xyNew = self.xyPos + vec
        if self.grid.rectContains(xyNew):
            self.xyPos = xyNew

            if xyNew in self.xyPathNodes:
                self.xyPathNodes = self.xyPathNodes[: self.xyPathNodes.index(xyNew)+1]
            else:
                self.xyPathNodes.append(xyNew)

            self.pathDraws = self.parent.pathToDraws(self.xyPathNodes)[1:]

    def jumpTo(self, xyNew):
        if self.grid.rectContains(xyNew):
            self.xyPos = xyNew
            self.refreshAutoPath()

    def refreshAutoPath(self):
        pass

    def drawContents(self, ren):
        for pathDraw in self.pathDraws:
            ren.drawChar( pathDraw, "!", fg = self.fgDebug )
        super().drawContents(ren)

    def pathTiles(self):
        return [self.grid.lookup(xyPathNode) for xyPathNode in self.xyPathNodes]

class ExamineCursor(GridCursor):
    fgDebug = (255, 255, 0)

class SelectAttackCursor(TrailCursor):
    fgDebug = (255, 0, 0)
