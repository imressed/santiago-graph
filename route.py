from helpers import generate_unique_id
from edge import CalculatedEdge


class Route:
    '''
    Route class represents an instance of route for our graph. it has information
    about start, end and way points for this route. It also gives information about
    hierarchy of route and road direction.

    Attributes:
        id: A UUID that act as a unique identifier for route
        start_point: a Point instance that represents start point of route
        end_point: a Point instance that represents end point of route
        waypoints: a list of Point instances that represents waypoints in route. Order counted!
        hierarchy: a integer that reperesents a hierarchy of route (expected values 1-5 ?)
        directed: a boolean if False route is bidirectional, if True route direction from start_point to end_point
    '''
    def __init__(self, points, edge, split=False):
        self.id = generate_unique_id()
        self.hierarchy = edge.hierarchy
        if split:
            self._init_splited_points(points, edge)
        else:
            self.directed = False
            self._init_points(points, edge)

    def _init_splited_points(self, points, edge):
        self.directed = edge.direction
        self.edge = edge
        for point in points:
            point.edge_id = edge.edge_id
        self.start_point = points[0]
        self.end_point = points[-1]
        self.waypoints = points[1:-1]

    def _init_points(self, points, edge):
        direction = edge.direction
        self.edge = edge
        if direction == 1:
            self.directed = True
        elif direction == -1:
            self.directed = True
            points.reverse()
        self.start_point = points[0]
        self.end_point = points[-1]
        self.waypoints = points[1:-1]

    def _split_array_by_item(self, arr, item, new_item):
        return arr[:arr.index(item)]+[new_item], [new_item]+arr[arr.index(item)+1:]

    def _split_array_by_segment(self, arr, segment, new_item):
        pass

    def split_edge_by_new_point(self, segment, point):
        points = [self.start_point] + self.waypoints + [self.end_point]


    def check_one_by_one_order(self, point_start, point_end):
        points = [self.start_point] + self.waypoints + [self.end_point]
        index_diff = abs(points.index(point_start) - points.index(point_end))
        if index_diff is not 1:
            return False
        return True

    def split_edge(self, old_point, new_point):
        new_point.from_me.extend([item for item in old_point.from_me if item not in new_point.from_me])
        new_point.to_me.extend([item for item in old_point.to_me if item not in new_point.to_me])
        points = [self.start_point] + self.waypoints + [self.end_point]
        if old_point == self.start_point:
            self.start_point = new_point
            return {'edge':self.edge, 'route':self, 'changed':False}
        elif old_point == self.end_point:
            self.end_point = new_point
            return {'edge':self.edge, 'route':self, 'changed':False}
        elif old_point in self.waypoints:
            edge1 = CalculatedEdge({'direction':self.edge.direction,
                                    'hierarchy':self.edge.hierarchy,
                                    'speed_indicators':self.edge.speed_indicators})
            edge2 = CalculatedEdge({'direction':self.edge.direction,
                                    'hierarchy':self.edge.hierarchy,
                                    'speed_indicators':self.edge.speed_indicators})
            new_points1, new_points2 = self._split_array_by_item(points, old_point, new_point)
            route1 = Route(new_points1, edge1, split=True)
            route2 = Route(new_points2, edge2, split=True)
            return {1:{'edge':edge1, 'route':route1},
                    2:{'edge':edge2, 'route':route2},
                    'changed':True}
