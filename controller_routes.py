import pickle, sys
from routes import Routes


def save_to_file(data, filename='test_dump'):
    sys.setrecursionlimit(100000)
    pickle.dump(data, open(filename, 'wb'))

def get_from_file(filename):
    return pickle.load(open(filename,'rb'))

if __name__ == '__main__':
    routes = Routes("dump_routes_after_near_points_error_fix_v2")
    print("routes: {0}".format(len(routes._routes)))
    print("points: {0}".format(len(routes._points)))
    print("enique points: {0}".format(len(set(routes._points))))
    print("edges: {0}".format(len(routes._edges)))


    r = get_from_file('dump_routes')
    print("routes: {0}".format(len(r)))

    for key,value in routes._edges.items():
        if key not in r.keys():
            print(key)

    for key,value in r.items():
        if key not in routes._edges.keys():
            print(key)


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
