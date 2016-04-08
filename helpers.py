import math
import itertools
from functools import wraps
from scipy.spatial import distance
from time import time
from uuid import uuid4

def timed(f):
    '''
    Decorator for calculating execution time of wraped function
    '''
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        print ("%s took %d sec to finish" % (f.__name__, elapsed))
        return result
    return wrapper

def generate_unique_id():
    '''
    generates a random UUID
    '''
    return uuid4()

def neighbours(items, direction=0, fill=None):
    '''
    Yeild the elements with their neighbours as (before, element, after).
    neighbours([1, 2, 3]) --> (None, 1, 2), (1, 2, 3), (2, 3, None)
    '''
    before = itertools.chain([fill], items)
    after = itertools.chain(items, [fill])
    next(after)
    return zip(items, before, after)


def euclidean(vector1, vector2):
    '''
    Use scipy to calculate euclidean distance
    '''
    dist = distance.euclidean(vector1, vector2)
    return dist

def line_magnitude(x1,y1,x2,y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
    return lineMagnitude

def distance_point_line (px, py, x1, y1, x2, y2):
    '''
    Calculate minimum distance from a point(px,py) to a line segment(x1,y1,x2,y2)
    '''
    LineMag = line_magnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        # just for test! if conditions are satisfied, its mean that nearest point to segment
        # is the beginning or ending of the segment, and this is the problem of another class.
        return 9999999999999
        #------------------
        
        ix = line_magnitude(px, py, x1, y1)
        iy = line_magnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = line_magnitude(px, py, ix, iy)

    return DistancePointLine

def segment_intersection(line1, line2):
    '''
    Calculate the intersection point of 2 segments
    '''
    def ccw(A,B,C):
        return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

    if not ccw(line1[0],line2[0],line2[1]) != ccw(line1[1],line2[0],line2[1]) and ccw(line1[0],line1[1],line2[0]) != ccw(line1[0],line1[1],line2[1]):
        return False

    xdiff = (line1[0].x - line1[1].x, line2[0].x - line2[1].x)
    ydiff = (line1[0].y - line1[1].y, line2[0].y - line2[1].y)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*[[line1[0].x,line1[0].y],[line1[1].x,line1[1].y]]), det(*[[line2[0].x,line2[0].y],[line2[1].x,line2[1].y]]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
