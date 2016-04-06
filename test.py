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
        return arr[:arr.index(segment[0])]+[item], [item]+arr[arr.index(segment[1])+1:]
    else:
        return arr[:arr.index(segment[1])]+[item], [item]+arr[arr.index(segment[0])+1:]

print(func([1,2,3,4,5,6],[3,4],9))
print(func([1,2,3,4,5,6],[3,2],9))
print('asfasfasf')
