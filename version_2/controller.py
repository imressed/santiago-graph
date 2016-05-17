import pandas as pd
from helpers import timed, euclidean
from point import Point


XCELLS = 100000 # number of x cells
YCELLS = 100000 # number of y cells

max_x = 4249623422
min_x = 2536497904

max_y = 63569714121
min_y = 62065572485


@timed
def get_edges():
    #load edges from dump
    EJES = pd.read_csv('../EJES.csv')
    edges = dict()
    for index, row in EJES.iterrows():
        #dictionary of edges, key - edge_id; value - edge parameters
        edges[int(row['id_eje'])] = {
            'id': index,
            'edge_id': int(row['id_eje']),
            'hierarchy': int(row['hierarchy']),
            'street_id': int(row['fename_id']),
            'length': row['Shape_Leng'],
            'direction': int(row['dir']),
            'speed_indicators': {
                'max_speed': row['V_LIBRE'],
                'trafic_jam_speed': row['V_PEAK'],
                'noramal_speed': row['V_VALLE'],
                'walking_speed': row['V_CAM']
            }
        }
    return edges

@timed
def get_points_set_and_points_list_and_segments(edges):
    # read points from dumps
    ALL_POINTS = pd.read_csv('../ALLPOINT.csv')

    # if u want to recompile min-max values for x and y coordinates, uncoment next 4 rows
    # print("max X = {}".format(max(ALL_POINTS.iterrows(), key=lambda x: x[1]['X'])))
    # print("min X = {}".format(min(ALL_POINTS.iterrows(), key=lambda x: x[1]['X'])))
    # print("max Y = {}".format(max(ALL_POINTS.iterrows(), key=lambda x: x[1]['Y'])))
    # print("min Y = {}".format(min(ALL_POINTS.iterrows(), key=lambda x: x[1]['Y'])))

    points_dict = dict()
    points_set = set()
    points_list = list()
    segments = list()
    # initialize empty initial point
    previous_point = Point()



    for index, row in ALL_POINTS.iterrows():
        point = Point(index, row['X'], row['Y'], row['id_eje'])
        current_edge = edges[point.edge_id]
        # calculate segment. first check if current point has the same edge with previous one.
        if point.edge_id == previous_point.edge_id:
            #then check the direction of edge of this point. if direction is 0 - bidirectional, add for both cases
            if current_edge['direction'] == 1 or current_edge['direction'] == 0:
                segments.append({
                    'from': previous_point,
                    'to':point,
                    'hierarchy': current_edge['hierarchy'],
                    'street_id': current_edge['street_id'],
                    'edge_id': current_edge['edge_id'],
                    'length': euclidean((previous_point.x,previous_point.y),(point.x,point.y))
                })
            if current_edge['direction'] == -1 or current_edge['direction'] == 0:
                segments.append({
                    'from': point,
                    'to': previous_point,
                    'hierarchy': current_edge['hierarchy'],
                    'street_id': current_edge['street_id'],
                    'edge_id': current_edge['edge_id'],
                    'length': euclidean((previous_point.x,previous_point.y),(point.x,point.y))
                })
        previous_point = point

        #set of unique points in dump
        points_set.add(point)
        #list of all points in dump
        points_list.append(point)


    return points_set, points_list, segments

if __name__ == '__main__':

    edges = get_edges()

    st, lst, segments = get_points_set_and_points_list_and_segments(edges)

    print(len(st))
    print(len(lst))


    # for item in segments:
    #     print('edge Id - {}'.format(item['edge_id']))
    #     print('edge Dir - {}'.format(edges[item['edge_id']]['direction']))
    #     print('from {}'.format(item['from']))
    #     print('to   {}'.format(item['to']))
