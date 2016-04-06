from copy import deepcopy
from points import Points
from point import CalculatedPoint
from edges import Edges
from edge import CalculatedEdge
from route import Route
from helpers import timed, segment_intersection


class Routes:
    '''
    Routes class acts as controller and collector for points and edges. It gets
    all the points and edges and convert them into usable form.

    Methods:
        get_routes: invokes with no parameters and returns a list of Route class instances.
    '''

    _edges = dict()
    _routes = dict()
    _points = list()

    def __init__(self):
        self._points, self._edges = Points('points_dump_with_neighbors').get_points_edges()
        self._calculate_routes()

    def _add_route(self, waypoints, id):
        edge = self._edges[id]
        route = Route(waypoints,edge)
        self._routes[id] = route

    def split_edges(self, new_point, points_arr):
        for item in points_arr:
            old_point = item
            route = self._routes[old_point.edge_id]

            result = route.split_edge(old_point=old_point, new_point=new_point)
            if old_point is not new_point:
                self._points[self._points.index(old_point)] = self._points[self._points.index(new_point)]
            if result['changed']:
                self._edges.pop(old_point.edge_id, None)
                self._routes.pop(old_point.edge_id, None)
                self._edges[result[1]['edge'].edge_id] = result[1]['edge']
                self._edges[result[2]['edge'].edge_id] = result[2]['edge']
                self._routes[result[1]['edge'].edge_id] = result[1]['route']
                self._routes[result[2]['edge'].edge_id] = result[2]['route']
            else:
                self._routes[result['edge'].edge_id] = result['route']

    def fix_intersection(self,segment1, segment2):

        
        # validating intersection classes, fix not work now!


        # if segment1[1].edge_id != segment1[0].edge_id:
        #     return False
        # if segment2[1].edge_id == segment2[0].edge_id:
        #     return False

        intersection_point = segment_intersection(segment1, segment2)

        new_point = CalculatedPoint(intersection_point[0], intersection_point[1], segment1[0].hierarchy)

        route1 = self._routes[segment1[0].edge_id]
        route2 = self._routes[segment2[1].edge_id]

        result1 = route1.split_edge_by_new_point(segment1, new_point)
        result2 = route2.split_edge_by_new_point(segment2, new_point)

        if result1:
            self._edges.pop(segment1[0].edge_id, None)
            self._routes.pop(segment1[0].edge_id, None)
            self._edges[result1[1]['edge'].edge_id] = result1[1]['edge']
            self._edges[result1[2]['edge'].edge_id] = result1[2]['edge']
            self._routes[result1[1]['edge'].edge_id] = result1[1]['route']
            self._routes[result1[2]['edge'].edge_id] = result1[2]['route']

        if result2:
            self._edges.pop(segment2[0].edge_id, None)
            self._routes.pop(segment2[0].edge_id, None)
            self._edges[result2[1]['edge'].edge_id] = result2[1]['edge']
            self._edges[result2[2]['edge'].edge_id] = result2[2]['edge']
            self._routes[result2[1]['edge'].edge_id] = result2[1]['route']
            self._routes[result2[2]['edge'].edge_id] = result2[2]['route']

    def check_one_by_one_order_in_path(self, point_start, point_end):
        if point_start.edge_id != point_end.edge_id:
            return False
        route = self._routes[point_start.edge_id]
        result = route.check_one_by_one_order(point_start, point_end)
        return result

    @timed
    def _calculate_routes(self):
        edge_id = 1
        waypoints = []
        for point in self._points:
            if point.edge_id != edge_id:
                self._add_route(waypoints, edge_id)
                waypoints = []
                edge_id = point.edge_id
            waypoints.append(point)

    def get_routes(self):
        return self._routes

    def get_points_edges(self):
        return self._points, self._edges
