from points import Points
from near_points_error import NearPointsError


if __name__ == '__main__':
    error_handler = NearPointsError()

    counter = 1
    length = len(error_handler.get_ds_result())

    print(error_handler._routes.get_routes()['209525'])

    for item in error_handler.get_ds_result():
        print('{0} of {1}'.format(counter, length))
        counter += 1
        error_handler.merge_points(item)

    error_handler.reset_classes_for_points_disjoint_set()
    pairs = 0
    tripple = 0
    more_than_2 = 0
    alone = 0

    for item in error_handler.get_ds_result():
        if len(item) == 1:
            alone += 1
        elif len(item) == 2:
            pairs += 1
        elif len(item) == 3:
            tripple += 1
        elif len(item) > 2:
            more_than_2 += 1
        print([it.edge_id for it in item])
    print("\n So, we have\n Standalone points:      {0}".format(alone))
    print("Classes with 2 points:       {0}".format(pairs))
    print("Classes with 3 points:       {0}".format(tripple))

    print("Classes with more than 2 points:     {0}".format(more_than_2))

'''
    print(len(error_handler.get_classes()))
    for key, value in error_handler.get_classes().items():
        print(key)
        for val in value:
            print(val.edge_id, val.x, val.y)
        break
'''
