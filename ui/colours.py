import random, math

DISCO_BRIGHT = 128
DISCO_DARK = 255

def randomDisco(bright, dark):
    med = math.floor((bright + dark) / 2)
    return random.choice([ (bright, med, med), (med, med, bright), (med, bright, med), (bright, bright, dark), (bright, bright, dark), (bright, dark, bright), (med, med, med) ])