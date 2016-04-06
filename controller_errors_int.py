from intersections_error import IntersectionsError

if __name__ == '__main__':

    error_handler = IntersectionsError()

    for key,value in error_handler.get_classes().items():
        print('{0} class'.format(key))

    print(len(error_handler.get_classes()))
