import actions, rsignals, tiles

class Hero(tiles.Occupant, actions.Actor):
    drawChar = "@"

    def tryRequestAction(self):
        return rsignals.ActionInputRequired(self)
