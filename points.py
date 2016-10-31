import pickle
import sys
import pandas as pd
from point import Point
from edges import Edges
import helpers
from helpers import timed, generate_unique_id, neighbours


ALL_POINTS = pd.read_csv('ALLPOINTTEST.csv')
XCELLS = 100000 # number of x cells
YCELLS = 100000 # number of y cells


class Points:
    '''
    Points class allow us to collect all the points from ALLPOINT.csv file and
    save them as an instances of Point class.

    Methods:
        get_points: invokes with no parameters, returns an array of Point class instances.
        save_to_file: save a list of Point instances to file named points, you can change the path file by setting filename attribute
    '''
    _points = list()

    def __init__(self, points_filename=''):
        self._points = []
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        if points_filename:
            self._get_from_file(points_filename)
        self._edges = Edges(edges_filename='edges_dump').get_edges()
        if len(self._points) is 0:
            self._collect_points()
        self._set_map_classes_for_points()

    def _add_point(self, point):
        self._points.append(point)

    def get_points(self):
        return self._points

    def get_points_edges(self):
        return self._points, self._edges

    @timed
    def _get_from_file(self, filename):
        self._points = pickle.load(open(filename,'rb'))
        self._set_min_max_from_retrieved_data()

    def save_to_file(self, filename='points'):
        sys.setrecursionlimit(100000)
        pickle.dump(self._points, open(filename, 'wb'))
	
	def update_to_file(self, filename='routes'):
        sys.setrecursionlimit(10)
		sys.update(10)
        pickle.dump(self._points, open(filename, 'wb'))
	
	
    def _init_min_max_values(self,row):
        self.min_y = row['Y']
        self.max_y = row['Y']
        self.max_x = row['X']
        self.min_x = row['X']

    def _set_min_max_values(self, row):
        if row['Y'] < self.min_y:
            self.min_y = row['Y']
        elif row['Y'] > self.max_y:
            self.max_y = row['Y']

        if row['X'] < self.min_x:
            self.min_x = row['X']
        elif row['X'] > self.max_x:
            self.max_x = row['X']

    def _set_min_max_from_retrieved_data(self):
        points = self.get_points()
        self.min_y = points[0].y
        self.max_y = points[0].y
        self.max_x = points[0].x
        self.min_x = points[0].x
        for row in points:
            if row.y < self.min_y:
                self.min_y = row.y
            elif row.y > self.max_y:
                self.max_y = row.y

            if row.x < self.min_x:
                self.min_x = row.x
            elif row.x > self.max_x:
                self.max_x = row.x

    @timed
    def _set_map_classes_for_points(self):
        diff_x = self.max_x - self.min_x
        diff_y = self.max_y - self.min_y

        step_x = diff_x // XCELLS
        step_y = diff_y // YCELLS

        for point in self._points:
            x_cell = (point.x - self.min_x) // step_x
            y_cell = (point.y - self.min_y) // step_y
            point_cell = (y_cell * YCELLS + x_cell)
            point.set_cell(point_cell)

    def _add_points(self,points):
        start_point = Point(points[0], role='start', is_waypoint=False)
        self._add_point(start_point)

        for point in points[1:-1]:
            point = Point(point)
            self._add_point(point)

        end_point = Point(points[-1], role='end', is_waypoint=False)
        self._add_point(end_point)

    def _set_neighbors(self, edge_id):
        direction = self._edges[edge_id].direction
        items = [item for item in self.get_points() if item.edge_id == edge_id]
        for item in neighbours(items):
            if direction == 0:
                if item[1] is not None:
                    item[0].add_from_me_node(item[1])
                    item[0].add_to_me_node(item[1])
                if item[2] is not None:
                    item[0].add_from_me_node(item[2])
                    item[0].add_to_me_node(item[2])
            elif direction == 1:
                if item[1] is not None:
                    item[0].add_to_me_node(item[1])
                if item[2] is not None:
                    item[0].add_from_me_node(item[2])
            elif direction == -1:
                if item[1] is not None:
                    item[0].add_from_me_node(item[1])
                if item[2] is not None:
                    item[0].add_to_me_node(item[2])

    @timed
    def _collect_points(self):
        '''
        iterate through points array, for each edge it sets start point,
        end point and waypoints. Sets maximum and minimum for x and y coordinates.
        Also this method set classes for points depending on x and y coordinate.
        '''
        flag = True
        edge_id = 1
        waypoints = []
        for index, row in ALL_POINTS.iterrows():
            print('{0} row'.format(index))
            if flag:
                self._init_min_max_values(row)
                flag = False

            if row['id_eje'] != edge_id:
                self._add_points(waypoints)
                self._set_neighbors(edge_id)
                waypoints = []
                edge_id = row['id_eje']
            self._set_min_max_values(row)
            waypoints.append(row)
