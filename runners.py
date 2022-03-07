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
            self.state.tryAdvance(self.interf)