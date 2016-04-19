from routes import Routes


if __name__ == '__main__':
    routes = Routes()
    p, e = routes.get_points_edges()
    i = 0
    print(p[-1].edge_id)
    print(routes.get_routes()[209524])
    print(routes.get_routes()[209525])

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
