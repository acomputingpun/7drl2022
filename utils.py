import re

def interp3(rgb1, dist, rgb2):
    return (
        int(rgb1[0] + (rgb2[0]-rgb1[0])*dist),
        int(rgb1[1] + (rgb2[1]-rgb1[1])*dist),
        int(rgb1[2] + (rgb2[2]-rgb1[2])*dist)
    )

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return mag(x1-x2, y1-y2)
def distPy(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return magPy(x1-x2, y1-y2)
def distMan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return magMan(x1-x2, y1-y2)
def dist3(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return mag3(x1-x2, y1-y2)
def dist4(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return mag4(x1-x2, y1-y2)

def mag(x, y):
    return mag4(x, y)
def magPy(x, y):
    return (x*x+y*y)**0.5
def magMan(x, y):
    return abs(x)+abs(y)
def mag3(x, y):
    return max(abs(x), abs(y)) + 0.5 * min(abs(x), abs(y))
def mag4(x, y):
    return max(abs(x), abs(y))

def allPoses(s, e):
    xs, ys = s
    xe, ye = e
    poses = []
#    print ("calling allPoses for", (s, e), "got", xs, ys, xe, ye)
    for y in range(ys, ys+ye):
        for x in range(xs, xs+xe):
#            print ("e", (x,y))
            poses.append((x, y))
#    print ("P", poses)
    return poses

def range2(e):
    return allPoses((0,0),e)

def rectContains(rect, xy):
    (rx, ry), (rsx, rsy) = rect
    x, y = xy
    return rx <= x < rx+rsx and ry <= y < ry+rsy

def rectConstrain(rect, xy):
    (rx, ry), (rsx, rsy) = rect
    x, y = xy
    return (median3( rx, x, rx+rsx-1), median3( ry, y, ry+rsy-1))

def rectShift(rect, xy):
    (rx, ry), (rsx, rsy) = rect
    x, y = xy
    return (median3(rx, x, x-rsx), median3(ry, y, y-rsy))

def linearShift(start, size, point):
    return median3(start, point, point-size)

def median3(x, y, z):
    return x+y+z - min(x, y, z) - max(x, y, z)

def wrapString(text, width):
    lines = []
    while text != "":
        lines.append( text[:width] )
        text = text[width:]
    return lines

def wrapText(text, width):
    lines = [""]
    for tokenMatch in re.finditer(r'(\n|[ \t\r\f\v]+|[^\s]+)', text):
        token = tokenMatch[0]
        if re.match(r'\n', token):
            lines.append("")
        elif re.match(r'\s', token) and len(lines[-1]) + len(token) > width:
            pass
        elif len(lines[-1]) + len(token) > width:
            while len(token) > width:
                lines.append(token[:width])
                token = token[width:]
            lines.append(token)
        else:
            lines[-1] = lines[-1] + token
    return lines

def wrapTextLine(text, width):
    wrapped = wrapText(text, width)
    return wrapped[0], wrapped[1:]

def dictToInstance(dict):
    class IDict():
        pass
    instance = IDict()
    for key in dict.keys():
        setattr(instance, key, dict[key])
    return instance

def interp(scalar, start, end):
    return ((end - start) * scalar) + start
def avalanche(value):
    return ~((~(value + 31991919191)) * value)

def bresenham(x,y):
    if x < 0:
        return [(-xy[0],xy[1]) for xy in bresenham(-x, y)]
    elif y < 0:
        return [(xy[0],-xy[1]) for xy in bresenham(x, -y)]
    elif y>x:
        return [(xy[1],xy[0]) for xy in bresenham(y, x)]
    elif x == 0:
        return [(0,0)]
    else:
        grad = y/x
        return [(xCur, round(xCur*grad)) for xCur in range(x+1)]