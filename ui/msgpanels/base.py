import vecs, math, xchars
from .. import scions, animas

class BaseMessagePanel(scions.Panel):
    xyAnchor = (1, 1)
    _panelSize = vecs.Vec2(43, 6)

    def drawOutline(self, ren):
        for xyDraw in self.allDraws():
            ren.drawChar( xyDraw, " ", fg =(216, 216, 216), bg = (0, 25, 0))

class SpecialMessagePanel(BaseMessagePanel):
    def drawContents(self, ren):
        pass

class MessagePanel(BaseMessagePanel):
    def __init__(self, *args):
        super().__init__(*args)
        self.curMessages = []

    def drawContents(self, ren):
        yDraw = 0
        for message in self.curMessages[-self.panelSize.y:]:
            ren.drawChar( (0, yDraw), ">")
            visiblePlaintext = message.visiblePlaintext()
            ren.drawText( (2, yDraw), visiblePlaintext)
            if (message.frac() < 1):
                ren.drawXChar( (len(visiblePlaintext)+1, yDraw), xchars.BLOCK)
            yDraw += 1

    def postPlaintext(self, plaintext):
        self.postMessage(Message(plaintext))

    def postMessage(self, message):
#        if len(self.curMessages) >= self.panelSize.y:
#            self.parent.afxMessageInterrupt()
        self.curMessages.append(message)
        message.register(self.interf)

class Message(animas.Anima):
    perCharMS = 6

    def __init__(self, plaintext):
        self.plaintext = plaintext

        self.maxMS = self.perCharMS * len(self.plaintext)

    def visibleChars(self):
        return math.floor(self.MS() / self.perCharMS)
    def periodic(self):
        return self.MS() % 30 < 15

    def visiblePlaintext(self):
        return self.plaintext[:self.visibleChars()]