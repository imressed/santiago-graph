from copy import deepcopy
from points import Points
from edges import Edges
from edge import CalculatedEdge
from route import Route
from helpers import timed


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

    def split_edges(self,new_point, points_arr):
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

    def split_edge_by_new_point(self,edge_segment, new_point_coordinates):

        if edge_segment[0].edge_id != edge_segment[1].edge_id:
            return False

        new_point = deepcopy(edge_segment[0])
        new_point.x = new_point_coordinates[0]
        new_point.y = new_point_coordinates[1]

        route = self._routes[edge_segment[0].edge_id]
        result = route.split_edge_by_new_point(edge_segment, new_point)
        # not finished

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
