class Scion():
    children = tuple()
    parent = None
    xyAnchor = (0,0)
    zLevel = 0

    def __init__(self, parent):
        self.parent = parent

    def draw(self, ren):
        self.drawOutline(ren)
        self.drawContents(ren)
        self.drawChildren(ren)

    def drawOutline(self, ren):
        raise NotImplementedError()
    def drawContents(self, ren):
        raise NotImplementedError()

    def drawChildren(self, ren):
        xyOrigin = ren.xyOffset
        zLevel = ren.zLevel
        for child in self.children:
            ren.xyOffset = xyOrigin + child.xyAnchor
            ren.zLevel = zLevel + child.zLevel
            child.draw(ren)

    @property
    def ancestor(self):
        return self.parent.ancestor
    @property
    def interf(self):
        return self.ancestor.interf

class Panel(Scion):
    _panelSize = (1,1)

    def drawOutline(self, ren):
        for x in range(self.panelSize.x):
            ren.drawChar((x, 0), "x" )
            ren.drawChar((x, self.panelSize.y-1), "x" )

        for y in range(self.panelSize.y):
            ren.drawChar((0, y), "x" )
            ren.drawChar((self.panelSize.x-1, y), "x" )

    @property
    def panelSize(self):
        return self._panelSize

class Flyer(Scion):
    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        raise NotImplementedError()
