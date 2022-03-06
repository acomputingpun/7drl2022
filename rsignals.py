class Signal():
    pass

class Advance(Signal):
    pass

class Intercession(Signal):
    def __init__(self, blockingEntity):
        self.blockingEntity = blockingEntity

class ActionIntercession(Intercession):
    pass
class ActionCompleted(ActionIntercession):
    pass
class ActionNotStarted(ActionIntercession):
    pass


class ActorIntercession(Intercession):
    pass
class ActionRequired(ActorIntercession):
    pass

class ZoneIntercession(Intercession):
    pass