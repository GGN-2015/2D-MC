import time

import Config
import Method
import Player

map_of_objects = {}
amo_list = [] # 当前的子弹序列
dead_list_of_objects = []

def set_block(block_x, block_y):
    global map_of_objects
    if map_of_objects.get((block_x, block_y)) == None:
        map_of_objects[(block_x, block_y)] = "ITEM_BLOCK"

def shoot_amo(pos, dir_vec, speed = Config.AMO_SPEED): # amo = (pos_x, pos_y, vec_valocity, shoot_time)
    global amo_list
    dir_vec = Method.vec_mul(Method.normalize(dir_vec), speed) # 得到速度向量
    if len(amo_list) < Config.AMO_MAX:
        amo_list.append((pos[0], pos[1], dir_vec, time.time(), Player.get_weapon_name())) # 记录当前射出子弹的时刻

def test_new_pos(new_pos, old_pos): # 检测新的位置是否能走过去
    global map_of_objects
    new_x, new_y = new_pos
    old_x, old_y = old_pos
    block_new_x, block_new_y = Method.get_block_xy(new_x, new_y)
    block_x, block_y = Method.get_block_xy(old_x, old_y)
    if(block_y == block_new_y and block_x == block_new_x): # 在同一个格子里爱怎么走怎么走
        return new_x, new_y
    else:
        if map_of_objects.get((block_new_x, block_new_y)) != None: # 有障碍物
            return old_x, old_y
        else:
            # 没有障碍物，什么都不用做
            return new_x, new_y

def get_dxdy(): # 计算屏幕的边距
    dW = Config.SCREEN_SIZE[0] // 2
    dH = Config.SCREEN_SIZE[1] // 2
    return (dW, dH)

def get_maxlen(): # 屏幕对角线距离
    return Method.distance((0, 0), Config.SCREEN_SIZE)

def crash_block(pos_x, pos_y): # 检测子弹是否达到了墙
    global dead_list_of_objects
    block_x, block_y = Method.get_block_xy(pos_x, pos_y)
    if map_of_objects.get((block_x, block_y)) != None:
        btype = map_of_objects[(block_x, block_y)]
        if btype in Config.DESTROYABLE:
            # dead_list_of_objects.append(map_of_objects[(block_x, block_y)])
            del map_of_objects[(block_x, block_y)] # 子弹能直接拆墙
        return True
    else:
        return False
