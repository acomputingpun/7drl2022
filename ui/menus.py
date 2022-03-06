import vecs
from . import scions

class MenuItem():
    def __init__(self, name, data):
        self.name = name
        self.data = data

class Menu():
    def __init__(self):
        self.menuItems = []
        self.highlightedIndex = None

    @property
    def highlightedMenuItem(self):
        if self.selectedIndex is None:
            return None
        else:
            return self.menuItems[self.selectedIndex]

    def panelSize(self):
        return vecs.Vec2(30, 30)

class MenuPanel(scions.Panel):
    def __init__(self, menu):
        self.menu = menu

    def drawContents(self, ren):
        for (index, menuItem) in enumerate(self.menu.menuItems):
            ren.drawChar((2, index+2), ">")

    @property
    def panelSize(self):
        return self.menu.panelSize()
