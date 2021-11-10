map_of_objects = {}

def set_box(block_x, block_y):
    global map_of_objects
    if map_of_objects.get((block_x, block_y)) == None:
        map_of_objects[(block_x, block_y)] = "ITEM_BOX"
