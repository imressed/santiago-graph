from near_segment_error import NearSegmentError

if __name__ == '__main__':

    error_handler = NearSegmentError()


    print('Error classes: {0}'.format(len(error_handler.get_classes())))
    # print('start near segment error handling')
    # for key,value in error_handler.get_classes().items():
    #     print(value[0])
    #     print(value[1])
    #     error_handler.fix_intersection(value[0],value[1])
    #
    # print('finish intersection fix')
    # error_handler.reset_classes_for_points()
    # print('Error classes: {0}'.format(len(error_handler.get_classes())))
