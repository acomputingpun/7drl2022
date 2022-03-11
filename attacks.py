import vecs, dirconst

class AttackProfile():
    baseRange = 1
    linearRange = 0

    def _inRangePoses(self):
        height = self.baseRange
        for y in range( -height, height+1):
            width = height-abs(y)
            for x in range(-width, width+1):
                yield vecs.Vec2(x, y) 
        return

    def inRangePosesFrom(self, xyPos):
        return [ xyPos + rel for rel in self._inRangePoses() ]
    def inRangeTilesFrom(self, tile):
        return [ tile.relTile(rel) for rel in self._inRangePoses() if tile.relTile(rel) is not None ]

class BumpAttack(AttackProfile):
    baseRange = 1
    linearRange = 0

class StubBeam(AttackProfile):
    baseRange = 0
    linearRange = 5

class StubBullet(AttackProfile):
    baseRange = 3