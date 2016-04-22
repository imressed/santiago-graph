import pickle
import sys
from routes import Routes
from itertools import combinations
from helpers import timed, euclidean

MERGE_RADIUS = 10000 # 10,000 = 1m in this radius we'll merge the points


class NearPointsError:
    '''
    NearPointsError class splits all the points to sectors and then calculate euclidean
    distance for each pair of points in class. if the distance is less than 1 meter
    new point class is created.

    Methods:
        get_classes: returns a dictionary: key: class identifier; value: pair of points to be merged togather
        get_sectors: returns a dictionary: key: cell identifier; value: a list of Point instances for this cell
    '''
    _sectors = dict()
    _unsorted = list()
    _initial_edges = dict()
    _classes = dict()
    _result_ds = list()

    def __init__(self):
        self._routes = Routes('dump_routes_after_near_points_error_fix')
        self._unsorted, self._initial_edges = self._routes.get_points_edges()

        #self._set_classes_for_points() #to calculate classes without disjoint set
        self._set_classes_for_points_disjoint_set()

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
    def _map_to_sectors_disjoint_set(self):
        for point in self._unsorted:
            if point.cell in self._sectors:
                self._sectors[point.cell].append([point])
            else:
                self._sectors[point.cell] = [[point]]
        return self._sectors

    @timed
    def _set_classes_for_points(self):
        sectors = self._map_to_sectors()

        for key,value in sectors.items():
            print('calculating classes for sector: {0}'.format(key))
            for item in combinations(value, 2):
                distance_between_points = euclidean([item[0].x, item[0].y], [item[-1].x, item[-1].y])
                if distance_between_points < MERGE_RADIUS and item[0].hierarchy == item[-1].hierarchy:

                    self._classes[len(self._classes)] = item
                    #item[0].set_crossroad(item[-1])
                    #item[-1].set_crossroad(item[0])

    @timed
    def _set_classes_for_points_disjoint_set(self):
        sectors = self._map_to_sectors_disjoint_set()
        print(len(sectors))
        for key,value in sectors.items():
            sector = value
            print('calculating classes for sector: {0}'.format(key))
            for item in combinations(value, 2):
                distance_between_points = euclidean([item[0][0].x, item[0][0].y], [item[-1][0].x, item[-1][0].y])
                if distance_between_points < MERGE_RADIUS and item[0][0].hierarchy == item[-1][0].hierarchy:
                    sector = self._union(sector, item[0][0], item[-1][0])
            self._result_ds.extend(sector)

    # this func is just for testing reasons (resetting all the classes to check correct error handling)
    @timed
    def reset_classes_for_points_disjoint_set(self):
        self._unsorted, self._initial_edges = self._routes.get_points_edges()
        self._result_ds = []
        self._sectors = {}
        sectors = self._map_to_sectors_disjoint_set()
        print(len(sectors))
        for key,value in sectors.items():
            sector = value
            print('calculating classes for sector: {0}'.format(key))
            for item in combinations(value, 2):
                distance_between_points = euclidean([item[0][0].x, item[0][0].y], [item[-1][0].x, item[-1][0].y])
                if distance_between_points < MERGE_RADIUS and item[0][0].hierarchy == item[-1][0].hierarchy:
                    sector = self._union(sector, item[0][0], item[-1][0])
            self._result_ds.extend(sector)

    def get_classes(self):
        return self._classes

    def save_to_file(self, filename='dump_routes_after_near_points_error_fix'):
        sys.setrecursionlimit(100000)
        pickle.dump(self._routes, open(filename, 'wb'))

    def merge_points(self, arr):
        self._routes.split_edges(new_point=arr[0], points_arr=arr)

    def get_sectors(self):
        return self._sectors

    def get_ds_result(self):
        return self._result_ds
