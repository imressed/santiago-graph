import copy
import pandas as pd
from helpers import timed, euclidean, segment_intersection, distance_point_line
from itertools import combinations
from point import Point


XCELLS = 1000000 # number of x cells
YCELLS = 1000000 # number of y cells

MERGE_RADIUS = 10 # 10,000 = 1m in this radius we'll merge the points

max_x = 4249623422
min_x = 2536497904

max_y = 63569714121
min_y = 62065572485

points_index = 0


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

    #init variables for cells calculating
    diff_x = max_x - min_x
    diff_y = max_y - min_y
    step_x = diff_x // XCELLS
    step_y = diff_y // YCELLS

    points_set_dict = dict()
    points_set = set()
    points_list = list()
    segments = list()
    segments_dict = dict()
    # initialize empty initial point
    previous_point = Point()

    for index, row in ALL_POINTS.iterrows():
        #calculate cell for each point
        x_cell = (row['X'] - min_x) // step_x
        y_cell = (row['Y'] - min_y) // step_y
        point_cell = (y_cell * YCELLS + x_cell)

        # create current point
        point = Point(index, row['X'], row['Y'], row['id_eje'], point_cell)
        points_index = index
        #get edge, connected with this point
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

    for point in list(points_set):
        points_set_dict[(point.x,point.y)] = point

    for segment in segments:
        if segment['from'] in segments_dict:
            segments_dict[segment['from']].append(segment)
        else:
            segments_dict[segment['from']] = [segment]
        if segment['to'] in segments_dict:
            segments_dict[segment['to']].append(segment)
        else:
            segments_dict[segment['to']] = [segment]

    return points_set, points_list, segments, segments_dict, points_set_dict


@timed
def recalculate_segments_dict(segments, segments_dict):
    for segment in segments:
        if segment['from'] in segments_dict:
            segments_dict[segment['from']].append(segment)
        else:
            segments_dict[segment['from']] = [segment]
        if segment['to'] in segments_dict:
            segments_dict[segment['to']].append(segment)
        else:
            segments_dict[segment['to']] = [segment]


@timed
def map_points_to_sectors(points):
    sectors = {}
    for point in points:
        if point.cell in sectors:
            sectors[point.cell].append(point)
        else:
            sectors[point.cell] = [point]
    return sectors

def get_points_from_neighbor_sectors(sectors, current_sector_id):
    #get all the neighbour segments and add points from them to result_points
    result_points = []
    #current line
    result_points.extend(sectors[current_sector_id])
    if current_sector_id-1 in sectors:
        result_points.extend(sectors[current_sector_id-1])
    if current_sector_id+1 in sectors:
        result_points.extend(sectors[current_sector_id+1])
    #previous line
    if current_sector_id-YCELLS in sectors:
        result_points.extend(sectors[current_sector_id-YCELLS])
    if current_sector_id-YCELLS-1 in sectors:
        result_points.extend(sectors[current_sector_id-YCELLS-1])
    if current_sector_id-YCELLS+1 in sectors:
        result_points.extend(sectors[current_sector_id-YCELLS+1])
    #next line
    if current_sector_id+YCELLS in sectors:
        result_points.extend(sectors[current_sector_id+YCELLS])
    if current_sector_id+YCELLS-1 in sectors:
        result_points.extend(sectors[current_sector_id+YCELLS-1])
    if current_sector_id+YCELLS+1 in sectors:
        result_points.extend(sectors[current_sector_id+YCELLS+1])
    return result_points

@timed
def near_points_error(sectors, segments, points_set_dict):
    # track total number of error classes
    error_classes = 0
    #statistics
    points_substitution_dict = {}
    #iterate through each sector
    for key,values in sectors.items():
        #get points from all nearby sectors, including current
        points_array = get_points_from_neighbor_sectors(sectors, key)
        #iterate through each point in sector
        for point in values:
            #iterate through each point from neighbour sectors
            for neighbour_point in points_array:
                # if this is the same point, pass
                if neighbour_point.id == point.id:
                    continue
                #if the euclidean distance is less then MERGE_RADIUS and points has the same hierarchy, then merge this points
                if euclidean((neighbour_point.x, neighbour_point.y),(point.x,point.y)) < MERGE_RADIUS and \
                    edges[point.edge_id]['hierarchy'] == edges[neighbour_point.edge_id]['hierarchy']:
                    #get the origin point from points_set_dict
                    origin_point = points_set_dict[(point.x, point.y)]
                    #assign origin id for this point
                    point.id = origin_point.id
                    # track points substitution
                    if origin_point in points_substitution_dict.keys():
                        points_substitution_dict[origin_point].extend([point, neighbour_point])
                    else:
                        points_substitution_dict[origin_point] = [point, neighbour_point]
                    #assign origin id, x and y for this point
                    neighbour_point.id = origin_point.id
                    neighbour_point.x = origin_point.x
                    neighbour_point.y = origin_point.y
                    #increment error clusses counter
                    error_classes+=1
    print("Near Points Errors Log: total classes - {0}, fixed - {0}".format(error_classes))


@timed
def intersection_segments_error(sectors, segments, segments_dict, points_set_dict):
    # track total number of intersections in data
    intersections_classes = 0
    #track total number of fixed intersections
    fixed_intersections = 0
    #get number of added points
    global points_index
    # iterate through sectors and get items from each sector
    for key,value in sectors.items():
        # print(key)
        # assign points from sector to points_array
        points_array = value
        # init array of all segments in this sector
        current_segments_array = []
        for point in points_array:
            # if we have segments connected with current point in segments dict, add them to current_segments_array
            if point in segments_dict:
                current_segments_array.extend(segments_dict[point])
        # print("{0} p - {1} segm".format(len(points_array),len(current_segments_array)))
        # iterate through all pairs of segments from current_segments_array
        for segment_pair in combinations(current_segments_array, 2):
            # if the segments has different hierarchy, pass
            if segment_pair[0]['hierarchy'] != segment_pair[1]['hierarchy']:
                continue
            # check if this two segmetns intersect
            check_intersection = segment_intersection([segment_pair[0]['from'],segment_pair[0]['to']],[segment_pair[1]['from'],segment_pair[1]['to']])
            if check_intersection:
                # if the segmetns intersect, increment points_index and number of intersections_classes
                intersections_classes += 1
                points_index += 1
                # create new point on this intersection (hack! add edge_id for tracking hierarchy of created point)
                intersection_point = Point(points_index, check_intersection[0], check_intersection[1], segment_pair[0]['hierarchy'], key)
                # check if intersection point is not the end or start of first segment
                if intersection_point != segment_pair[0]['from'] and intersection_point != segment_pair[0]['to']:
                    # increment number of fixed intersections
                    fixed_intersections += 1
                    # make copy of end point of segment(create new object)
                    to_point = copy.deepcopy(segment_pair[0]['to'])
                    # change the end point of current segment to intersection_point
                    segment_pair[0]['to'] = intersection_point
                    # and recalculate segment length
                    segment_pair[0]['length'] = euclidean((intersection_point.x,intersection_point.y),(segment_pair[0]['from'].x,segment_pair[0]['from'].y))
                    # then create new segment starting in intersection_point and ending in initial segment end point
                    segments.append({
                        'from': intersection_point,
                        'to': to_point,
                        'hierarchy': segment_pair[0]['hierarchy'],
                        'street_id': segment_pair[0]['street_id'],
                        'edge_id': segment_pair[0]['edge_id'],
                        'length': euclidean((intersection_point.x,intersection_point.y),(to_point.x,to_point.y))
                    })
                    #update data with new point
                    points_set.add(intersection_point)
                    points_list.append(intersection_point)
                    points_set_dict[(intersection_point.x,intersection_point.y)] = intersection_point

                # check if intersection point is not the end or start of second segment
                if intersection_point != segment_pair[1]['from'] and intersection_point != segment_pair[1]['to']:
                    fixed_intersections += 1
                    to_point = copy.deepcopy(segment_pair[1]['to'])
                    segment_pair[1]['to'] = intersection_point
                    segment_pair[1]['length'] = euclidean((intersection_point.x,intersection_point.y),(segment_pair[1]['from'].x,segment_pair[1]['from'].y))
                    segments.append({
                        'from': intersection_point,
                        'to': to_point,
                        'hierarchy': segment_pair[1]['hierarchy'],
                        'street_id': segment_pair[1]['street_id'],
                        'edge_id': segment_pair[1]['edge_id'],
                        'length': euclidean((intersection_point.x,intersection_point.y),(to_point.x,to_point.y))
                    })
                    #update data with new point
                    points_set.add(intersection_point)
                    points_list.append(intersection_point)
                    points_set_dict[(intersection_point.x,intersection_point.y)] = intersection_point

    print("Intersections Errors Log: total classes - {0}, fixed - {1}".format(intersections_classes, fixed_intersections))


@timed
def near_segment_error(sectors,segments,segments_dict,points_set_dict):
    # track total number of intersections in data
    near_points_classes = 0
    #track total number of fixed intersections
    fixed_near_points = 0
    #get number of added points
    global points_index
    # iterate through sectors and get items from each sector
    for key,value in sectors.items():
        #print(key)
        # assign points from sector to points_array
        points_array = value
        # init array of all segments in this sector
        current_segments_array = []
        for point in points_array:
            # if we have segments connected with current point in segments dict, add them to current_segments_array
            if point in segments_dict:
                current_segments_array.extend(segments_dict[point])
        #print("{0} p - {1} segm".format(len(points_array),len(current_segments_array)))
        for point in points_array:
            for sector_segment in current_segments_array:
                if edges[point.edge_id]['hierarchy'] != sector_segment['hierarchy']:
                    continue
                distance_segment_point = distance_point_line(point.x, point.y,
                                                            sector_segment['from'].x, sector_segment['from'].y,
                                                            sector_segment['to'].x, sector_segment['to'].y)

                if distance_segment_point < MERGE_RADIUS:
                    near_points_classes += 1
                    if point != sector_segment['from'] and point != sector_segment['to']:
                        fixed_near_points += 1
                        to_point = copy.deepcopy(sector_segment['to'])
                        # change the end point of current segment to intersection_point
                        sector_segment['to'] = point
                        # and recalculate segment length
                        sector_segment['length'] = euclidean((point.x,point.y),(sector_segment['from'].x,sector_segment['from'].y))
                        # then create new segment starting in intersection_point and ending in initial segment end point
                        segments.append({
                            'from': point,
                            'to': to_point,
                            'hierarchy': sector_segment['hierarchy'],
                            'street_id': sector_segment['street_id'],
                            'edge_id': sector_segment['edge_id'],
                            'length': euclidean((point.x,point.y),(to_point.x,to_point.y))
                        })
    print("Near Segment Errors Log: total classes {0}, fixed {1}".format(near_points_classes, fixed_near_points))


if __name__ == '__main__':

    edges = get_edges()

    points_set, points_list, segments, segments_dict, points_set_dict = get_points_set_and_points_list_and_segments(edges)

    sectors = map_points_to_sectors(points_list)

    near_points_error(sectors, segments, points_set_dict)

    intersection_segments_error(sectors,segments,segments_dict,points_set_dict)

    recalculate_segments_dict(segments, segments_dict)

    near_segment_error(sectors,segments,segments_dict,points_set_dict)


    # for item in segments:
    #     print('edge Id - {}'.format(item['edge_id']))
    #     print('edge Dir - {}'.format(edges[item['edge_id']]['direction']))
    #     print('from {}'.format(item['from']))
    #     print('to   {}'.format(item['to']))
