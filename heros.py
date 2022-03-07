import actions, rsignals, tiles

class Hero(tiles.Occupant, actions.Actor):
    drawChar = "@"

    def tryRequestAction(self):
        raise rsignals.ActionInputRequired(self)
