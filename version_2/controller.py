import pandas as pd
from point import Point


# read points and edges from dumps
ALL_POINTS = pd.read_csv('../ALLPOINTTEST.csv')
EJES = pd.read_csv('../EJES.csv')

points_set = set()
points_list = list()
segments = list()

def get_edges():
    edges = dict()
    for index, row in EJES.iterrows():
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

def get_points_set_and_points_list_and_segments():
    current_point_id = 0

if __name__ == '__main__':

    edges = get_edges()

    print(edges)
