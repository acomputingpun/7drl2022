#import renderers.canvas.tcdraw as tcdraw
#import renderers.asciiwindowed.tcdraw as tcdraw
import renderers.rlsdl.tcdraw as tcdraw
#import renderers.terminal.tcdraw as tcdraw

import states
import ui.interfaces as interfaces

class Runner():
    def __init__(self):
        self.state = states.State()
        self.interf = interfaces.Interface(tcdraw, self.state)

    def mainLoop(self):
        while True:
            self.state.advance(self.interf)
