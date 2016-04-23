from routes import Routes


if __name__ == '__main__':
    routes = Routes('dump_routes_after_near_points_error_fix')
    print(routes)
    p, e = routes.get_points_edges()
    r = routes._routes
    print(r)
    for k,v in r.items():
        print("k,   v".format(k,v))


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
