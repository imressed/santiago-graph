from helpers import euclidean, segment_intersection, neighbours
import pickle

#print(line_intersection( ( (0,0), (3,3) ), ( (0,1), (0,2) ) ) )

#for item in neighbours([1,2,3,4,5,6], direction=0):
    #print (item)

#points = pickle.load(open('points','rb'))
#for point in points:
    #print(point.edge_id, point.role, point.from_me, point.to_me)


#print (segment_intersection( [[1,1],[3,3]], [[1,1],[3,2]] ) )

def func(arr, segment, item):
    if arr.index(segment[0]) < arr.index(segment[1]):
        return arr[:arr.index(segment[0])+1]+[item], [item]+arr[arr.index(segment[1]):]
    else:
        return arr[:arr.index(segment[1])+1]+[item], [item]+arr[arr.index(segment[0]):]

def segment_intersection(line1, line2):
    '''
    Calculate the intersection point of 2 segments
    '''
    def ccw(A,B,C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

    if not ccw(line1[0],line2[0],line2[1]) != ccw(line1[1],line2[0],line2[1]) and ccw(line1[0],line1[1],line2[0]) != ccw(line1[0],line1[1],line2[1]):
        return False

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*[[line1[0][0],line1[0][1]],[line1[1][0],line1[1][1]]]), det(*[[line2[0][0],line2[0][1]],[line2[1][0],line2[1][1]]]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

print(segment_intersection([[1,1],[3,3]],[[2,2],[1,3]]))
