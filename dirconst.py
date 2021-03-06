import vecs

UP = N = vecs.Vec2(0, -1)
RIGHT = E = vecs.Vec2(1, 0)
DOWN = S = vecs.Vec2(0, 1)
LEFT = W = vecs.Vec2(-1, 0)
IN_PLACE = vecs.Vec2(0, 0)

CARDINALS = [UP, RIGHT, DOWN, LEFT]
VALIDS = [UP, RIGHT, DOWN, LEFT, IN_PLACE]

NW = vecs.Vec2(-1, -1)
NE = vecs.Vec2(1, -1)
SW = vecs.Vec2(-1, 1)
SE = vecs.Vec2(1, 1)

DIAGONALS = [NW, NE, SW, SE]
OCTAGONALS = CARDINALS + DIAGONALS
NONAGONALS = VALIDS + DIAGONALS

CARDINAL_COMPONENTS = {NW: [UP, LEFT], NE: [UP, RIGHT], SW: [DOWN, LEFT], SE: [DOWN, RIGHT], UP: [UP], LEFT: [LEFT], RIGHT: [RIGHT], DOWN:[DOWN], IN_PLACE: [] }

ROT_CW = ROTATE_CW = { UP : RIGHT, RIGHT : DOWN, DOWN : LEFT, LEFT : UP, NW:NE, NE:SE, SE:SW, SW:NW }
ROT_CCW = ROTATE_CCW = { UP : LEFT, LEFT : DOWN, DOWN : RIGHT, RIGHT : UP, NE:NW, SE:NE, SW:SE, NW:SW }
REVERSE = {UP : DOWN, DOWN : UP, RIGHT : LEFT, LEFT : RIGHT, NE:SW, NW:SE, SE:NW, SW:NE }

def orientFromFacing(vec, facing):
    if facing == N or facing == IN_PLACE:
        return vec
    elif facing == E:
        return vec.rotCW90()
    elif facing == W:
        return vec.rotCCW90()
    elif facing == S:
        return vec.rot180()
    else:
        raise Exception()

def deorientFromFacing(vec, facing):
    if facing == N or facing == IN_PLACE:
        return vec
    elif facing == E:
        return vec.rotCCW90()
    elif facing == W:
        return vec.rotCW90()
    elif facing == S:
        return vec.rot180()
    else:
        raise Exception()