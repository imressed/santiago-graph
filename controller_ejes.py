from edges import Edges


if __name__ == '__main__':
    rng = 5
    edges = Edges(edges_filename='edges_dump').get_edges()

    print(edges[1])

    for index, edge in edges.items():
        print(index)
        print(edge.speed_indicators)
        break
