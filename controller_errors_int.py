from intersections_error import IntersectionsError

if __name__ == '__main__':

    error_handler = IntersectionsError()

    print('start intersection fix')
    print('Error classes: {0}'.format(len(error_handler.get_classes())))
    for key,value in error_handler.get_classes().items():

        error_handler.fix_intersection(value[0],value[1])
    print('finish intersection fix')
    error_handler.reset_classes_for_points()
    print('Error classes: {0}'.format(len(error_handler.get_classes())))
