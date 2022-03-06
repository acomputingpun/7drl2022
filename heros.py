import actions, rsignals

class Hero(actions.Actor):
    def tryRequestAction(self):
        return rsignals.ActorIntercession(self)

    def iSubmitAction(self, action):
        self._submitAction(action)
