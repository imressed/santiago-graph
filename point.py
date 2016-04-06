from helpers import generate_unique_id

class Point:
    '''
    Point class represents a single node in graph. It has information about coordinates of node
    in UTM system (UTM standart: WGS84, UTM zone: 19s). Also each point has arrays
    that represents all the points that can be accessible from this node, and that
    can get access. Other accessable parameters are descibed below.

    Attributes:
        id: A UUID that act as a unique identifier for Point
        x: An integer (UTM value), represents x coordinate
        y: An integer (UTM value), represents y coordinate
        from_me: A list of Point instances that represents nodes that can be accessable form this node
        to_me: A list of Point instances that represents nodes that can get access to this node
        is_waypoint: A boolean represents if this node is a waypoint or not
        cell: A integer that represents a unique cell on map for this point
        role: [Depricated] A string that represent role of this point
        edge_id: a integer that represents initial edge for this Point
        new_edge_id: a integer that represents new edge for this Point (usage: new_edge_id = 0 ? edge_id: new_edge_id)
        hierarchy: a integer that reperesents a hierarchy of route (expected values 1-5 ?)

    Methods:
        set_cell: requires cell:int, set cell for this Point
        add_from_me_node: requires point:Point, append new from_me Point
        add_to_me_node: requires point:Point, append new to_me Point
        is_waypoint: requires choise:bool, set is_waypoint
        set_new_edge: requires edge_id:int, set new edge for this Point
    '''
    def __init__(self, data, role='waypoint', is_waypoint='True'):
        data = dict(data)
        self.id = generate_unique_id()
        self.x = data['X']
        self.y = data['Y']
        self.hierarchy = data['hierarchy']
        self.edge_id = data['id_eje']
        self.new_edge_id = []
        #self.fename_id = data['fename_id']
        self.role = role
        self.cell = 0
        self.from_me = []
        self.to_me = []
        self.is_waypoint = is_waypoint

    def set_cell(self, cell):
        self.cell = cell

    def add_from_me_node(self, point):
        self.from_me.append(point)

    def add_to_me_node(self,point):
        self.to_me.append(point)

    def is_waypoint(self, choise):
        self.is_waypoint = choise

    def add_new_edge(self, edge_id):
        self.new_edge_id.append(edge_id)
