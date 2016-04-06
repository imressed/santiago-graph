from routes import Routes
from itertools import combinations
from helpers import timed, segment_intersection

MERGE_RADIUS = 10000 # 10,000 = 1m in this radius we'll merge the points


class IntersectionsError:
    '''
    IntersectionsError class splits all the points to sectors and then check if
    any sector in class intersects with another. if we detect this intersection,
    we create a new point in this intersection

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

    def _find(self, sector, el):
        for point in sector:
            if el in point:
                return sector.index(point)

    def _union(self, sector, el1, el2):
        index_element_1 = self._find(sector, el1)
        index_element_2 = self._find(sector, el2)
        if index_element_1 != index_element_2:
            sector[index_element_2] = sector[index_element_1]+sector[index_element_2]
            del sector[index_element_1]
        return sector

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
            for item in combinations(points_combinations, 2):
                intersection = segment_intersection(item[0], item[-1])
                if intersection: # and item[0][0].edge_id != item[1][0].edge_id: if only different edge can intersect
                    self._classes[len(self._classes)] = item
                    # test on map intersections
                    print ('hierarchy {0}'.format(item[0][0].hierarchy))

    # this func is just for testing reasons (resetting all the classes to check correct error handling)
    @timed
    def reset_classes_for_points(self):
        self._unsorted, self._initial_edges = self._routes.get_points_edges()
        self._sectors = {}
        sectors = self._map_to_sectors()
        for key,value in sectors.items():
            points_combinations = [item for item in combinations(value, 2)
                                        if (item[0].edge_id == item[1].edge_id) and
                                        self._routes.check_one_by_one_order_in_path(item[0],item[1])]
            for item in combinations(points_combinations, 2):
                intersection = segment_intersection(item[0], item[-1])
                if intersection and item[0][0].hierarchy == item[0][1].hierarchy: # and item[0][0].edge_id != item[1][0].edge_id: if only different edge can intersect
                    self._classes[len(self._classes)] = item

    def get_classes(self):
        return self._classes

    def fix_intersection(self, segment1, segment2):
        self._routes.fix_intersection(segment1, segment2)
