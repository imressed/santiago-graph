

class Point(object):

    def __init__(self, id, x, y, edge_id):
        self.id = id
        self.x = x
        self.y = y
        self.edge_id = edge_id

    def __hash__(self):
        return (self.x, self.y)
