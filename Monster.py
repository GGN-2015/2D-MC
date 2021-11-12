import math
import pygame
import random
import time

# import Astar
import Config
import Game
import Map
import Method
import Player

monster_list = []               # 僵尸队列, monster = ((pos_x, pos_y), "MONSTER_TYPE", hit_point, monster_id)
monster_target = {
    # 记录当前怪物的前进方向目标点
}
dead_list = []                  # 死亡的僵尸队列, monster = ((pos_x, pos_y), "MONSTER_TYPE", dead_time)
last_monster = time.time()      # 记录上次生成 Monster 的时间

monster_count = 0 # 统计怪物的总数

def crash_monster(pos_x, pos_y, vec_dir): # vec_dir 记录子弹的速度向量
    global monster_list
    crashed = False
    new_monster_list = []
    for monster_pos, mtype, hp, ID in monster_list:
        if Method.circle_crash((pos_x, pos_y), Config.AMO_R, monster_pos, Config.MONSTER_R[mtype]): # 计算圆交是否存在
            crashed = True
            hp -= 1
            monster_pos = Method.vec_add(monster_pos, Method.vec_mul(vec_dir, Config.HIT_BACK)) # 击退
        if hp <= 0: # 僵尸死亡
            dead_list.append((monster_pos, mtype, time.time())) # 添加死亡僵尸
            Player.player_score += Config.MONSTER_SCORE
        else:
            new_monster_list.append((monster_pos, mtype, hp, ID)) # 追加到新的僵尸序列中
    monster_list = new_monster_list
    return crashed

def add_monster(monster_pos, mtype, hp): # 追加一个怪物
    global monster_list
    global last_monster
    global monster_count
    monster_count += 1
    if len(monster_list) < Config.MONSTER_MAX:
        monster_list.append((monster_pos, mtype, hp, monster_count))
        last_monster = time.time()

def not_reach(pos_xy, monster_id):
    """判断怪物是否到达了目标点"""
    if  monster_target.get(monster_id) == None: # 没有目标的人，活着就是目标实现了
        return True
    else:
        return Method.distance(pos_xy, monster_target[monster_id]) < Config.POSITION_EPS

def check_monster_crash_player(): # 检测是否有僵尸打到了玩家
    cnt = 0
    for pos_xy, mtype, hit_point, monster_id in monster_list:
        if Method.circle_crash(Player.get_position(), Config.PLAYER_R, pos_xy, Config.MONSTER_R[mtype]):
            cnt += 1
    Player.damage(cnt) # 让玩家掉血

def get_monster_dir(monster_pos, monster_id): # 计算怪物当前的朝向
    # global monster_target
    # if Method.not_in_screen(monster_pos, Player.get_position()):  # 对于不在屏幕里的怪物直接朝着玩家走
    #     return Method.normalize(Method.vec_sub(Player.get_position(), monster_pos))
    # else:
    #     if monster_target.get(monster_id) != None and not_reach(monster_pos, monster_id): # 对于有目标的怪物，不用重新制作目标了
    #         pass
    #     else:
    #         if Method.in_midddle(monster_pos): # 没有目标结点
    #             astar = Astar.Astar(monster_pos, Player.get_position())
    #             monster_target[monster_id] = astar.solve()
    #         else:
    #             monster_target[monster_id] = Method.get_mid_of_block(Method.get_block_xy(*monster_pos))
    #     return Method.normalize(Method.vec_sub(monster_target[monster_id], monster_pos)) # 向着目标前进

    return Method.normalize(Method.vec_sub(Player.get_position(), monster_pos)) # 向着玩家前进

    # else:
    #     astar = Astar.Astar(monster_pos, Player.get_position())
    #     return astar.solve() # 根据算法找到最优路径

def move_monster(): # 将所有 Monster 向前移动一定长度
    global monster_list
    new_monster_list = []
    for monster_pos, mtype, hp, monster_id in monster_list: # monster ID
        # delta_vec = Method.vec_mul(Method.normalize(Method.vec_sub(Player.get_position(), monster_pos)), Config.MONSTER_SPEED())
        delta_vec = Method.vec_mul(get_monster_dir(monster_pos, monster_id), Config.MONSTER_SPEED())
        new_pos = Method.vec_add(monster_pos, delta_vec)
        monster_pos = Map.test_new_pos(new_pos, monster_pos)
        if hp > 0:
            new_monster_list.append((monster_pos, mtype, hp, monster_id))
    monster_list = new_monster_list
    # print(len(monster_list)) # 打印怪物的总数

def draw_moster(screen, mid_x, mid_y, monster_type):
    pos_in_screen = Method.get_screen_pos((mid_x, mid_y), Player.get_position())
    pygame.draw.circle(screen, Config.MONSTER_COLOR, pos_in_screen, Config.MONSTER_R[monster_type], width = Config.MONSTER_LINE_WIDTH)
    vec = Method.vec_sub(Player.get_position(), (mid_x, mid_y))
    if vec != (0, 0): # 绘制怪物鼻子
        # print(vec)
        Game.draw_nose(screen, pos_in_screen, vec, Config.MONSTER_R[monster_type], Config.MONSTER_COLOR, Config.MONSTER_LINE_WIDTH)

def create_monster_demo(): # 演示性制造僵尸
    if time.time() - last_monster >= Config.MONSTER_SPAN and Config.MONSTER_OK:
        x, y = Method.random_near_position(Player.position_x, Player.position_y, Map.get_maxlen() // 2, Map.get_maxlen() * 2)
        if Method.not_in_screen((x, y), Player.get_position()): # 只在地图外生成僵尸
            add_monster((x, y), "MONSTER_ZOMBIE", random.randint(3, 5))

def draw_dead_moster(screen, pos_x, pos_y, mtype, alpha):
    pos_in_screen = Method.get_screen_pos((pos_x, pos_y), Player.get_position())
    color_now = Method.average(Config.MONSTER_COLOR, Config.WHITE, alpha)
    pygame.draw.circle(screen, color_now, pos_in_screen, Config.MONSTER_R[mtype], width = Config.MONSTER_LINE_WIDTH)

def draw_all_moster(screen):
    global dead_list
    global monster_list
    if Config.GAME_RUNNING: # 游戏结束后不要再移动 monster
        move_monster()
    new_monster_list = []
    for monster_pos, mtype, hp, ID in monster_list:
        if Method.in_sight(monster_pos, Player.get_position(), Map.get_dxdy()):
            draw_moster(screen, monster_pos[0], monster_pos[1], mtype)
            new_monster_list.append((monster_pos, mtype, hp, ID))
        else:
            if Method.distance(monster_pos, Player.get_position()) >= 2 * Map.get_maxlen(): # 对距离太远的僵尸进行 despwan
                pass
            else:
                new_monster_list.append((monster_pos, mtype, hp, ID))
    monster_list = new_monster_list

    new_dead_list = []
    for monster_pos, mtype, dead_time in dead_list:
        alpha = 1 - (time.time() - dead_time) / Config.MONSTER_FADE_TIME # 当前僵尸的透明度
        if alpha > 0:
            draw_dead_moster(screen, monster_pos[0], monster_pos[1], mtype, alpha)
            new_dead_list.append((monster_pos, mtype, dead_time))
        else:
            # don't show it
            pass
    dead_list = new_dead_list
        