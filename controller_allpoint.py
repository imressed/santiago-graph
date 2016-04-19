from points import Points


if __name__ == '__main__':
    points = Points('points_dump_with_neighbors')

    points_iterator = points.get_points()

    print(points.max_x, points.min_x)
    print(points.max_y, points.min_y)

    i = 0
    print(points_iterator[-1].edge_id)

    # for point in points_iterator:
    #     #print ('edge_id {0}, {3} \n from_me {1} \n to-me {2}'.format(point.edge_id, point.from_me, point.to_me, point.role))
    #     print('edge_id {0}, role {1}, {2} {3} {4}'.format(point.edge_id, point.role, point.x, point.y, point.cell))
