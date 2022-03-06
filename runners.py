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
            rSignal = self.state.tryAdvance()
            if isinstance(rSignal, rsignals.Advance):
                "todo: If the state is capable of zero-tick advancing, have it do so."
                "todo: (the state advancing will usually instantly kick the ball back to the interface, creating animas or something)"
                "todo: tryAdvance() returns False iff the attempt to try advancing fails - meaning we need inteface interaction of some kind."
            elif isinstance(rSignal, rsignals.Intercession):
                "todo: Otherwise, the state is waiting on us or the interface for input of some kind.  We should provide it."
                "todo: 'Input of some kind' could be just a 0-tick acknolwedgement from us or the interface that the state is changing."
                "todo: either way, we probably redraw."

                if isinstance(rSignal, rsignals.ActionCompleted):
                    rSignal.blockingEntity.rCleanup()
                elif isinstance(rSignal, rsignals.ActionNotStarted):
                    rSignal.blockingEntity.rStart()
                elif isinstance(rSignal, rsignals.ActorIntercession):
                    "todo: We need a player-inputted command from the interface (probably to submit an action)"
                else:
                    pass
                self.interf.advance()
            else:
                raise Exception()