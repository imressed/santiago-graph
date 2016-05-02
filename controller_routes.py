import pickle, sys
from routes import Routes


def save_to_file(data, filename='test_dump'):
    sys.setrecursionlimit(100000)
    pickle.dump(data, open(filename, 'wb'))

def get_from_file(filename):
    return pickle.load(open(filename,'rb'))

if __name__ == '__main__':
    routes = Routes("dump_near_points_error_final_as_dict")
    print("routes: {0}".format(len(routes._routes)))
    print("points: {0}".format(len(routes._points)))
    print("enique points: {0}".format(len(set(routes._points))))
    print("edges: {0}".format(len(routes._edges)))


    r = get_from_file('dump_routes')
    print("routes: {0}".format(len(r)))

    for key,value in routes._edges.items():
        if key not in routes._routes.keys():
            print(key)

    for key,value in routes._routes.items():
        if key not in routes._edges.keys():
            print(key)

    # dump = get_from_file('test_dump')
    # print("routes: {0}".format(len(dump['routes'])))
    # print("points: {0}".format(len(dump['points'])))
    # print("enique points: {0}".format(len(set(dump['points']))))
    # print("edges: {0}".format(len(dump['edges'])))


    # for key, route in routes.items():
    #     print(route.directed)
    #     print(route.start_point.role, route.start_point.edge_id)
    #     print(route.end_point.role, route.end_point.edge_id)
    #
    #     for way in route.waypoints:
    #         print(way.role, way.edge_id)
    #     i += 1
    #     if i > 100:
    #         break
