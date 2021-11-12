import time

import Config
import Map
import Method
import Player

map_of_objects = {}
amo_list = [] # 当前的子弹序列
dead_list_of_objects = []

last_aid_block = time.time()

def random_set_aid_box():
    global last_aid_block
    if time.time() - last_aid_block >= Config.AID_BOX_SPAN:
        x, y = Method.random_near_position(Player.position_x, Player.position_y, Map.get_maxlen() // 2, Map.get_maxlen() * 2)
        bx, by = Method.get_block_xy(x, y)
        set_aid_box(bx, by)
        last_aid_block = time.time()

def set_aid_box(block_x, block_y):
    global map_of_objects
    if map_of_objects.get((block_x, block_y)) == None:
        map_of_objects[(block_x, block_y)] = "ITEM_AID_BOX"
        # print("set aid_box at", (block_x, block_y)) # prompt

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

def no_block_between(monster_pos, player_pos): # 计算直线上是否有障碍物
    dx = player_pos[0] - monster_pos[0]
    dy = player_pos[1] - monster_pos[1]
    vec_dir = Method.normalize((dx, dy)) # 计算得到相对方向
    pbx, pby = Method.get_block_xy(*Player.get_position())
    cnt = round(Method.distance((dx, dy), (0, 0))) // Config.BLOCK_SIZE
    for i in range(1, cnt + 2):
        vec_now = Method.vec_add(monster_pos, Method.vec_mul(vec_dir, i * Config.BLOCK_SIZE / 2)) # 当前考虑位置的坐标
        bx, by = Method.get_block_xy(*vec_now)
        if map_of_objects.get((bx, by)) != None:
            btype = map_of_objects[(bx, by)]
            if btype not in Config.TRANSPARENT: # 不透明
                return False
        if (bx, by) == (pbx, pby):
            break
    return True

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
