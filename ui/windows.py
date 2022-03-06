from . import scions

class Window(scions.Panel):
    def __init__(self, interf):
        self._interf = interf

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        pass

    @property
    def ancestor(self):
        return self
    @property
    def interf(self):
        return self._interf

class BlankWindow(Window):
    pass