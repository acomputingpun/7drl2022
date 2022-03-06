from . import warps, windows
#from . import warps, windows, gridpanels, syspanels, nonpanels, attpanels, messages, backpanels, animas
#from . import fx
#import random

class GameWindow(windows.Window):
    def __init__(self, interf):
        super().__init__(interf)

#        self.gridPanel = gridpanels.GridPanel(self, interf.state.level.grid)
#        self.backPanel = backpanels.BackgroundPanel(self)
#        self.msgPanel = messages.MessagePanel(self)

#        self.children = [self.msgPanel, self.sysPanel, self.gridPanel, self.backPanel]

    def requestActionWarp(self):
        raise NotImplementedError()

    @property
    def hero(self):
        return self.interf.state.hero

class GameWindowWarp(warps.Warp):
    def warpArrowKey(self, key, shift = False):
        pass

    def warpOtherKey(self, key):
        if key == 113: # q
            pass
        elif key == 119: # w
            pass
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
        elif key == 9: # tab
            pass
        else:
            print ("Key was", key)