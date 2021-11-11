import time
import pygame
import random

import Config
import Game
import Map
import Method
import Player

monster_list = []               # 僵尸队列, monster = ((pos_x, pos_y), "MONSTER_TYPE", hit_point)
dead_list = []                  # 死亡的僵尸队列, monster = ((pos_x, pos_y), "MONSTER_TYPE", dead_time)
last_monster = time.time()      # 记录上次生成 Monster 的时间

def crash_monster(pos_x, pos_y, vec_dir): # vec_dir 记录子弹的速度向量
    global monster_list
    crashed = False
    new_monster_list = []
    for monster_pos, mtype, hp in monster_list:
        if Method.circle_crash((pos_x, pos_y), Config.AMO_R, monster_pos, Config.MONSTER_R[mtype]): # 计算圆交是否存在
            crashed = True
            hp -= 1
            monster_pos = Method.vec_add(monster_pos, Method.vec_mul(vec_dir, Config.HIT_BACK)) # 击退
        if hp <= 0: # 僵尸死亡
            dead_list.append((monster_pos, mtype, time.time())) # 添加死亡僵尸
        else:
            new_monster_list.append((monster_pos, mtype, hp)) # 追加到新的僵尸序列中
    monster_list = new_monster_list
    return crashed

def add_monster(monster_pos, mtype, hp): # 追加一个怪物
    global monster_list
    global last_monster
    if len(monster_list) < Config.MONSTER_MAX:
        monster_list.append((monster_pos, mtype, hp))
        last_monster = time.time()

def move_monster(): # 将所有 Monster 向前移动一定长度
    global monster_list
    new_monster_list = []
    for monster_pos, mtype, hp in monster_list:
        delta_vec = Method.vec_mul(Method.normalize(Method.vec_sub(Player.get_position(), monster_pos)), Config.MONSTER_SPEED)
        new_pos = Method.vec_add(monster_pos, delta_vec)
        monster_pos = Map.test_new_pos(new_pos, monster_pos)
        if hp > 0:
            new_monster_list.append((monster_pos, mtype, hp))
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
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        if Method.not_in_screen((x, y), Player.get_position()): # 只在地图外生成僵尸
            add_monster((x, y), "MONSTER_ZOMBIE", random.randint(3, 5))

def draw_dead_moster(screen, pos_x, pos_y, mtype, alpha):
    pos_in_screen = Method.get_screen_pos((pos_x, pos_y), Player.get_position())
    color_now = Method.average(Config.MONSTER_COLOR, Config.WHITE, alpha)
    pygame.draw.circle(screen, color_now, pos_in_screen, Config.MONSTER_R[mtype], width = Config.MONSTER_LINE_WIDTH)

def draw_all_moster(screen):
    global dead_list
    move_monster()
    for monster_pos, mtype, hp in monster_list:
        draw_moster(screen, monster_pos[0], monster_pos[1], mtype)
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
        