from helpers import pairing_func

class Point(object):

    def __init__(self, id=0, x=0, y=0, edge_id=0, cell=0):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.edge_id = int(edge_id)
        self.cell = int(cell)

    def __hash__(self):
        return hash((self.x,self.y))

    def __eq__(self, other):
        return hash((self.x,self.y)) == hash((other.x,other.y))
