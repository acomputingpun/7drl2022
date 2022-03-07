#import renderers.canvas.tcdraw as tcdraw
#import renderers.asciiwindowed.tcdraw as tcdraw
import renderers.rlsdl.tcdraw as tcdraw
#import renderers.terminal.tcdraw as tcdraw

import ui.interfaces as interfaces

import states, rsignals

class Runner():
    def __init__(self):
        self.state = states.State()
        self.interf = interfaces.Interface(tcdraw, self.state)

    def mainLoop(self):
        while True:
            if self.interf.hasBlockingAnimas():
                self.interf.advance()
            else:
                try:
                    self.state.tryAdvance(self.interf)
                except rsignals.ActionInputRequired as rSig:
                    self.interf.wtransferPlayerInput()
                    self.interf.debugShow(rSig)
                    self.interf.advance()
                except rsignals.ActionStart as rSig:
                    self.interf.wtransferAdvanceTime()
                    self.interf.debugShow(rSig)
                    self.interf.advance()
                except rsignals.Signal as rSig:
                    raise Exception("We don't know how to handle this signal:", rSig)