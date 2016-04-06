from routes import Routes


if __name__ == '__main__':
    routes = Routes().get_routes()
    i = 0
    print(routes)
    for key, route in routes.items():
        print(route.directed)
        print(route.start_point.role, route.start_point.edge_id)
        print(route.end_point.role, route.end_point.edge_id)

        for way in route.waypoints:
            print(way.role, way.edge_id)
        i += 1
        if i > 100:
            break
