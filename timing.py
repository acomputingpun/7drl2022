class __Timer():
    def __init__(self):
        self._initMS = None
        self._elapsedMS = 0
        self._frozenMS = None
    def pause(self):
        self._elapsedMS = self.innerMS()
        self._initMS = None
    def unpause(self):
        self._elapsedMS = self.innerMS()
        self._initMS = self.masterMS()
    def freeze(self):
        self._frozenMS = self.MS()
    def unfreeze(self):
        self._frozenMS = None

    def reset(self):
        if self._initMS is not None:
            self._initMS = self.masterMS()
        self._elapsedMS = 0

    def togglePause(self):
        if self.isPaused():
            self.unpause()
        else:
            self.pause()

    def innerMS(self):
        if self._initMS is None:
            return self._elapsedMS
        else:
            return (self.masterMS() - self._initMS) + self._elapsedMS
    def MS(self):
        if self._frozenMS is None:
            return self.innerMS()
        else:
            return self._frozenMS

    def isPaused(self):
        return self._initMS is None

    def masterMS(self):
        raise NotImplementedError()

    def slave(self):
        return SlaveTimer(self)

class SlaveTimer(__Timer):
    def __init__(self, master):
        super().__init__()
        self.master = master
    def masterMS(self):
        return self.master.MS()
