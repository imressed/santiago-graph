from helpers import pairing_func

class Point(object):

    def __init__(self, id, x, y, edge_id):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.edge_id = int(edge_id)

    def __hash__(self):
        return hash((self.x,self.y))

    def __eq__(self, other):
        return hash((self.x,self.y)) == hash((other.x,other.y))
