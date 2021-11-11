import importlib
from os import X_OK # reload 方法
import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN, KEYDOWN
import sys
import time

import Config
import Items
import Map
import Method
import Monster # 记录所有怪物的信息
import Player

def show_position(screen):
    x, y = Method.get_block_xy(Player.position_x, Player.position_y)
    Items.show_text(screen, (0, 0),'(%d,%d)' % (x, y)) # 在屏幕上 (0, 0) 位置显示一个字符串

def draw_base_lines(screen):
    px = Player.position_x % 50
    py = Player.position_y % 50 # x, y 为玩家所在的像素的位置, 由于玩家始终是游戏的中心，所以地图会相对运动
    screen.fill(Config.BACKGROUND_COLOR)

    R = Config.BLOCK_SIZE // 2 # 计算半径

    for i in range(0 - 1, Config.ROW_BLOCK_CNT + 2): # 绘制所有竖线
        x = i * Config.BLOCK_SIZE - px
        y_min = 0
        y_max = Config.SCREEN_SIZE[1] # 竖直高度
        pygame.draw.line(screen, Config.LINE_COLOR, (x - R, y_min), (x - R, y_max), Config.LINE_WIDTH)

    for i in range(0 - 1, Config.COLUMN_BLOCK_CNT + 2): # 绘制所有横线
        x_min = 0
        x_max = Config.SCREEN_SIZE[0] # 水平宽度
        y = i * Config.BLOCK_SIZE - py
        pygame.draw.line(screen, Config.LINE_COLOR, (x_min, y - R), (x_max, y - R), Config.LINE_WIDTH)

def draw_nose(screen, coord, vec, R, color, width): # 画生物的鼻子, vec 是速度方向
    from Method import vec_add
    from Method import vec_mul
    vec = Method.normalize(vec)
    start_delta_vec = vec_mul(vec, R // 3)
    end_delta_vec = vec_mul(vec, R // 2 * 3)
    pygame.draw.line(screen, color, vec_add(coord, start_delta_vec), vec_add(coord, end_delta_vec), width)
    # print(vec_add(coord, start_delta_vec), vec_add(coord, end_delta_vec))

def draw_player_nose(screen, coord, vec):
    draw_nose(screen, coord, vec, Config.PLAYER_R, Player.color_of_main, Config.PLAYER_LINE_WIDTH)

def draw_main_player(screen): # 在屏幕中心绘制主玩家
    R = Config.BLOCK_SIZE // 2
    mid_x = Config.SCREEN_SIZE[0] // 2
    mid_y = Config.SCREEN_SIZE[1] // 2
    pygame.draw.circle(screen, Player.color_of_main, (mid_x, mid_y), R, width = Config.PLAYER_LINE_WIDTH)

    mouse_x, mouse_y = pygame.mouse.get_pos() # 鼠标的坐标
    vec = (mouse_x - mid_x, mouse_y - mid_y)
    if vec != (0, 0):
        draw_player_nose(screen, (mid_x, mid_y), vec)

def move_event_check(): # 检测玩家运动事件
    from pygame.constants import K_a, K_s, K_d, K_w
    old_x, old_y = Player.position_x, Player.position_y
    # importlib.reload(Config)
    key_pressed = pygame.key.get_pressed() # 这里的移动算法并不是很完美
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        Player.position_x -= Config.SPEED
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        Player.position_x += Config.SPEED
    if key_pressed[K_s] or key_pressed[K_DOWN]: 
        Player.position_y += Config.SPEED
    if key_pressed[K_w] or key_pressed[K_UP]:
        Player.position_y -= Config.SPEED
    Player.position_x, Player.position_y = Map.test_new_pos((Player.position_x, Player.position_y), (old_x, old_y))

def set_event_check(event): # 检测放置事件并处理
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            block_x, block_y = Method.get_block_xy(Player.position_x, Player.position_y) # 计算 block 的位置
            Map.set_box(block_x, block_y) # 试图在 block_x, block_y 处放置一个箱子

def shoot_event_check(event):
    from pygame.constants import MOUSEBUTTONDOWN
    if event.type == MOUSEBUTTONDOWN: # shoot
        if time.time() - Player.last_fire_time > Config.WEAPON_REFRESH_TIME[Player.get_weapon_name()]: # 当前武器已经缓冲完毕
            if Player.amo_count[Player.get_weapon_name()] != 0:
                pos = event.pos # 获取鼠标在屏幕上的点击位置
                dW = Config.SCREEN_SIZE[0] // 2
                dH = Config.SCREEN_SIZE[1] // 2 # 玩家在屏幕上的位置
                vec = Method.vec_sub(pos, (dW, dH)) # 计算子弹速度方向
                if vec != (0, 0):
                    Map.shoot_amo((Player.position_x, Player.position_y), vec) # 从玩家位置发射子弹
                    Player.last_fire_time = time.time()
                    if Player.amo_count[Player.get_weapon_name()] > 0: # 子弹数有限制，不能无限使用
                        Player.amo_count[Player.get_weapon_name()] -= 1

def change_weapon_event_check(event):
    from pygame.constants import K_e
    if event.type == KEYDOWN:
        if event.key == K_e:
            Player.next_weapon() # 切换到下一把武器

def draw_items(screen):
    # Map.map_of_objects 中存放了所有东西的坐标
    block_x, block_y = Method.get_block_xy(Player.position_x, Player.position_y) # 计算 Player 所在的 block 的位置
    rcnt = Config.ROW_BLOCK_CNT // 2
    ccnt = Config.COLUMN_BLOCK_CNT // 2
    for i in range(-rcnt - 1, rcnt + 2):
        for j in range(-ccnt - 1, ccnt + 2):
            if Map.map_of_objects.get((block_x + i, block_y + j)) != None: # 能够找到这个位置的物品
                item_type = Map.map_of_objects[(block_x + i, block_y + j)]
                Items.draw_item(screen, item_type, (block_x + i, block_y + j), (Player.position_x, Player.position_y)) # Items 是材质包

def draw_amos(screen): # 绘制屏幕上的所有子弹
    # 每一个子弹是一个小球，有一个速度和一个位置
    dW = Config.SCREEN_SIZE[0] // 2
    dH = Config.SCREEN_SIZE[1] // 2 # 界面边界相对于玩家的距离
    new_amo_list = []
    for amo in Map.amo_list: # amo = (pos_x, pos_y, vec_valocity, shoot_time, amo_weapon)
        pos_x, pos_y, vec_valocity, shoot_time, amo_weapon = amo # 获取子弹的信息
        if Method.in_sight((pos_x, pos_y), (Player.position_x, Player.position_y), (dW, dH)):
            Items.draw_amo(screen, (pos_x, pos_y), (Player.position_x, Player.position_y)) # 在屏幕上绘制子弹

        crash = Monster.crash_monster(pos_x, pos_y, vec_valocity) # 检测子弹是否打中了怪物
        if time.time() - shoot_time < Config.AMO_SPAN[amo_weapon] and not crash:
            new_amo_list.append((pos_x + vec_valocity[0], pos_y + vec_valocity[1], vec_valocity, shoot_time, amo_weapon)) # 计算新的位置并加入子弹队列
    Map.amo_list = new_amo_list # 更新子弹序列
    # print(len(Map.amo_list)) # 显示新的子弹序列中元素个数

def show_message(screen, messages):
    nowH = 0
    for line in messages.split('\n'):
        if line != "": # 跳过所有信息中的空行
            Items.show_text(screen, (0, nowH), line) # 输出当前行消息
            nowH += Config.MESSAGE_HEIGHT
            

def draw_all(screen):        # 绘制全部对象
    draw_base_lines(screen)  # 绘制网格线
    draw_items(screen)       # 绘制地图上的物品
    # show_position(screen)    # 左上角显示玩家坐标
    draw_main_player(screen) # 绘制玩家
    draw_amos(screen)        # 绘制所有子弹
    show_message(screen, Player.get_message()) # 左上角显示玩家的各种信息
    Monster.draw_all_moster(screen) # 绘制所有怪物

# ! 需要将这个接口赋值成绘制背景图像的算法
draw_background = lambda screen: (draw_all(screen))

# ! 需要将这个接口赋值成事件处理工具
event_processor = lambda event: (set_event_check(event), shoot_event_check(event), change_weapon_event_check(event))

class Game:
    """定义游戏的主界面"""
    def __init__(self):
        """游戏初始化"""
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(Config.SCREEN_SIZE)   # 当前游戏的界面
        pygame.display.set_caption(Config.GAME_NAME)                # 显示标题

    def run_game(self):
        """开始游戏的主循环"""
        global draw_background
        global event_processor # ! 使用事件处理接口解决问题
        while True:
            for event in pygame.event.get(): # 检测所有事件
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    event_processor(event) # 用事件处理机制处理
                    pass
            move_event_check()
            Monster.create_monster_demo()
            draw_background(self.screen)
            pygame.display.flip() # 更新显示窗口内容

if __name__ == "__main__":
    game = Game()
    game.run_game()
