from intersections_error import IntersectionsError

if __name__ == '__main__':

    error_handler = IntersectionsError()


    print('Error classes: {0}'.format(len(error_handler.get_classes())))
    print('start intersection fix')
    for key,value in error_handler.get_classes().items():
        print("{2}, {0}, from_me: {1}".format(value[0][0], value[0][0].from_me, value[0][0].edge_id))
        for i in value[0][0].from_me:
            print(i.edge_id)
        print("{2}, {0}, from_me: {1}".format(value[0][1], value[0][1].from_me, value[0][1].edge_id))
        for i in value[0][1].from_me:
            print(i.edge_id)
        print("-----")
        print("{2}, {0}, from_me: {1}".format(value[1][0], value[1][0].from_me, value[1][0].edge_id))
        for i in value[1][0].from_me:
            print(i.edge_id)
        print("{2}, {0}, from_me: {1}".format(value[1][1], value[1][1].from_me, value[1][0].edge_id))
        for i in value[1][1].from_me:
            print(i.edge_id)
        print("-------------------------------------")
        # error_handler.fix_intersection(value[0],value[1])

    # print('finish intersection fix')
    # error_handler.reset_classes_for_points()
    # print('Error classes: {0}'.format(len(error_handler.get_classes())))
