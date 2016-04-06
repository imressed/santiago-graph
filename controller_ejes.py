from edges import Edges


if __name__ == '__main__':
    rng = 5
    edges = Edges().get_edges()
    for edge in edges:
        print(edges.index(edge))
        print(edge.speed_indicators)
        break
