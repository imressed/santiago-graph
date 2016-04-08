from routes import Routes
from itertools import combinations
from helpers import timed, distance_point_line

MERGE_RADIUS = 10000 # 10,000 = 1m in this radius we'll merge the points


class NearSegmentError:
    '''
    NearSegmentError divide all the points of sector to segments of existing in
    this sector edges and calculate distances to nearest point. if the distance
    is less than a constant, we add this point to segmet's route path.

    Methods:
        get_classes: returns a dictionary: key: class identifier; value: pair of points to be merged togather
        get_sectors: returns a dictionary: key: cell identifier; value: a list of Point instances for this cell
    '''
    
    _sectors = dict()
    _unsorted = list()
    _initial_edges = dict()
    _classes = dict()

    def __init__(self):
        self._routes = Routes()
        self._unsorted, self._initial_edges = self._routes.get_points_edges()
        self._set_classes_for_points()

    @timed
    def _map_to_sectors(self):
        for point in self._unsorted:
            if point.cell in self._sectors:
                self._sectors[point.cell].append(point)
            else:
                self._sectors[point.cell] = [point]
        return self._sectors

    @timed
    def _set_classes_for_points(self):
        sectors = self._map_to_sectors()

        for key,value in sectors.items():
            print('calculating classes for sector: {0}'.format(key))
            points_combinations = [item for item in combinations(value, 2)
                                        if (item[0].edge_id == item[1].edge_id) and
                                        self._routes.check_one_by_one_order_in_path(item[0],item[1])]
            for item in points_combinations:
                for point in value:
                    distance_point_segment = distance_point_line(point.x, point.y, item[0].x, item[0].y, item[1].x, item[1].y)
                    if distance_point_segment and distance_point_segment < MERGE_RADIUS:
                        self._classes[len(self._classes)] = {'segment':item, 'point': point}

    def get_classes(self):
        return self._classes
