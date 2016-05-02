from points import Points
from near_points_error import NearPointsError


if __name__ == '__main__':
    error_handler = NearPointsError()

    counter = 1
    length = len(error_handler.get_ds_result())

    print(error_handler._routes.get_routes()[int('209525')])

    for item in error_handler.get_ds_result():
        print('{0} of {1}'.format(counter, length))
        counter += 1
        error_handler.merge_points(item)


    error_handler.save_to_file()
    error_handler._routes.save_to_file()

    error_handler.reset_classes_for_points_disjoint_set()
    errors = dict()

    for item in error_handler.get_ds_result():
        if len(item) not in errors:
            errors[len(item)] = 1
        else:
            errors[len(item)] += 1

    for key, value in errors.items():
        print("Classes with {0} points:       {1}".format(key, value))

'''
    print(len(error_handler.get_classes()))
    for key, value in error_handler.get_classes().items():
        print(key)
        for val in value:
            print(val.edge_id, val.x, val.y)
        break
'''
