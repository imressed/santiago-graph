import pandas as pd
from helpers import timed
from point import Point


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

    points_dict = dict()
    points_set = set()
    points_list = list()
    segments = list()

    for index, row in ALL_POINTS.iterrows():
        #set of unique points in dump
        points_set.add( (row['X'],row['Y']) )
        #list of all points in dump
        points_list.append({
            'id': index,
            'edge_id': row['id_eje'],
            'x': row['X'],
            'y': row['Y']
        })
    return points_set, points_list

if __name__ == '__main__':

    edges = get_edges()

    st, lst = get_points_set_and_points_list_and_segments(edges)

    print(len(st))
    print(len(lst))
