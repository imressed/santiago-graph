from helpers import generate_unique_id


class Edge:
    '''
    Edge class represents and information about one edge in graph. it gives information
    about speed limits on this edge length of the path and other info listed below.

    Attributes:
        id: A UUID that act as a unique identifier for Edge
        edge_id: A integer, that represents unique id for this edge from EJES.csv file
        direction: A integer, that represents drive direction for this edge(expected values: 0: bidirectional; 1: from start to end point; -1: from end to start point)
        hierarchy: A integer, that reperesents a hierarchy of edge (expected values 1-5 ?)
        path_length: a integer, that represents length of this edge
        speed_indicators: A dictionary, with speed limitations for this edge:
            max_speed: A integer, represents maximum drive speed for this edge
            trafic_jam_speed: A integer, reperesents drive speed at trafic jam
            noramal_speed: A integer, represents avarage driving speed on this edge
            walking_speed: A integer, represents walking speed of passers
    '''

    def __init__(self, data):
        data = dict(data)
        self.id = generate_unique_id()
        self.edge_id = int(data['id_eje'])
        #self.fename_id = int(data['fename_id'])
        self.direction = int(data['dir'])
        self.hierarchy = int(data['hierarchy'])
        self.path_length = data['Shape_Leng']
        self.speed_indicators = dict()
        self.speed_indicators['max_speed'] = data['V_LIBRE']
        self.speed_indicators['trafic_jam_speed'] = data['V_PEAK']
        self.speed_indicators['noramal_speed'] = data['V_VALLE']
        self.speed_indicators['walking_speed'] = data['V_CAM']

class CalculatedEdge:
    '''
    Edge class represents and information about one edge in graph. it gives information
    about speed limits on this edge length of the path and other info listed below.

    Attributes:
        id: A UUID that act as a unique identifier for Edge
        edge_id: A integer, that represents unique id for this edge from EJES.csv file
        direction: A integer, that represents drive direction for this edge(expected values: 0: bidirectional; 1: from start to end point; -1: from end to start point)
        hierarchy: A integer, that reperesents a hierarchy of edge (expected values 1-5 ?)
        path_length: a integer, that represents length of this edge
        speed_indicators: A dictionary, with speed limitations for this edge:
            max_speed: A integer, represents maximum drive speed for this edge
            trafic_jam_speed: A integer, reperesents drive speed at trafic jam
            noramal_speed: A integer, represents avarage driving speed on this edge
            walking_speed: A integer, represents walking speed of passers
    '''

    def __init__(self, data):
        data = dict(data)
        self.id = generate_unique_id()
        self.edge_id = generate_unique_id()
        #self.fename_id = int(data['fename_id'])
        self.direction = int(data['direction'])
        self.hierarchy = int(data['hierarchy'])
        self.path_length = 'not implemented yet'
        self.speed_indicators = data['speed_indicators']
