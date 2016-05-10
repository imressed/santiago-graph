import pickle
import sys
import pandas as pd
from edge import Edge
from helpers import timed


EJES = pd.read_csv('EJES.csv')


class Edges:
    '''
    Edges class allow us to collect all the points from EJES.csv file and
    save them as an instances of Edge class.

    Methods:
        get_edges: returns a list of Edge class instances for all edges
        add_edge: requires an instance of Edge class, append new edge to edges collection
    '''
    _edges = dict()

    def __init__(self, edges_filename=''):
        self._edges = {}
        if edges_filename:
            self._get_from_file(edges_filename)
        if len(self._edges) is 0:
            self._collect_edges()

    def add_edge(self, edge):
        self._edges[edge.edge_id] = edge

    def delete_edge(self, edge_id):
        del self._edges[edge_id]
        return True

    def get_edges(self):
        return self._edges

    @timed
    def _get_from_file(self, filename):
        self._edges = pickle.load(open(filename,'rb'))

    def save_to_file(self, filename='edges'):
        sys.setrecursionlimit(100000)
        pickle.dump(self._edges, open(filename, 'wb'))

    @timed
    def _collect_edges(self):
        for index, row in EJES.iterrows():
            edge = Edge(row)
            self.add_edge(edge)
