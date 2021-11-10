import importlib
from os import X_OK # reload 方法
import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE, K_UP, K_DOWN, KEYDOWN
import sys

import Config
import Items
import Method
import Map

position_x = 0
position_y = 0 # 记录玩家所在的位置
color_of_main = (255, 0, 0) # 主人公的颜色

def show_position(screen):
    font = pygame.font.SysFont(Config.MESSAGE_FONT_NAME, Config.MESSAGE_FONT_SIZE) # 使用系统字体
    x, y = Method.get_block_xy(position_x, position_y)
    text = font.render('(%d,%d)' % (x, y), True, Config.MESSAGE_COLOR)
    screen.blit(text, (0, 0))

def draw_base_lines(screen):
    global position_x
    global position_y
    px = position_x % 50
    py = position_y % 50 # x, y 为玩家所在的像素的位置, 由于玩家始终是游戏的中心，所以地图会相对运动
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

def draw_player_nose(screen, coord, vec): # 画玩家鼻子, vec 是速度方向
    from Method import vec_add
    from Method import vec_mul

    vec = Method.normalize(vec)
    start_delta_vec = vec_mul(vec, Config.BLOCK_SIZE // 6)
    end_delta_vec = vec_mul(vec, Config.BLOCK_SIZE // 4 * 3)
    
    pygame.draw.line(screen, color_of_main, vec_add(coord, start_delta_vec), vec_add(coord, end_delta_vec), Config.PLAYER_LINE_WIDTH)
    # print(vec_add(coord, start_delta_vec), vec_add(coord, end_delta_vec))

def draw_main_player(screen): # 在屏幕中心绘制主玩家
    R = Config.BLOCK_SIZE // 2
    mid_x = Config.SCREEN_SIZE[0] // 2
    mid_y = Config.SCREEN_SIZE[1] // 2
    pygame.draw.circle(screen, color_of_main, (mid_x, mid_y), R, width = Config.PLAYER_LINE_WIDTH)

    mouse_x, mouse_y = pygame.mouse.get_pos() # 鼠标的坐标
    vec = (mouse_x - mid_x, mouse_y - mid_y)
    if vec != (0, 0):
        draw_player_nose(screen, (mid_x, mid_y), vec)

def test_new_pos(old_x, old_y):
    global position_x
    global position_y
    block_new_x, block_new_y = Method.get_block_xy(position_x, position_y)
    block_x, block_y = Method.get_block_xy(old_x, old_y)
    if(block_y == block_new_y and block_x == block_new_x): # 在同一个格子里爱怎么走怎么走
        pass
    else:
        if Map.map_of_objects.get((block_new_x, block_new_y)) != None: # 有障碍物
            position_x, position_y = old_x, old_y
        else:
            pass

def move_event_check(): # 检测玩家运动事件
    global position_x
    global position_y
    from pygame.constants import K_a, K_s, K_d, K_w
    old_x, old_y = position_x, position_y
    # importlib.reload(Config)
    key_pressed = pygame.key.get_pressed() # 这里的移动算法并不是很完美
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        position_x -= Config.SPEED
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        position_x += Config.SPEED
    if key_pressed[K_s] or key_pressed[K_DOWN]: 
        position_y += Config.SPEED
    if key_pressed[K_w] or key_pressed[K_UP]:
        position_y -= Config.SPEED
    test_new_pos(old_x, old_y)
    

def set_event_check(event): # 检测放置事件并处理
    if event.type == KEYDOWN:
        if event.key == K_SPACE:
            block_x, block_y = Method.get_block_xy(position_x, position_y) # 计算 block 的位置
            Map.set_box(block_x, block_y) # 试图在 block_x, block_y 处放置一个箱子

def draw_items(screen):
    # Map.map_of_objects 中存放了所有东西的坐标
    block_x, block_y = Method.get_block_xy(position_x, position_y) # 计算 block 的位置
    rcnt = Config.ROW_BLOCK_CNT // 2
    ccnt = Config.COLUMN_BLOCK_CNT // 2
    for i in range(-rcnt - 1, rcnt + 2):
        for j in range(-ccnt - 1, ccnt + 2):
            if Map.map_of_objects.get((block_x + i, block_y + j)) != None: # 能够找到这个位置的物品
                item_type = Map.map_of_objects[(block_x + i, block_y + j)]
                Items.draw_item(screen, item_type, (block_x + i, block_y + j), (position_x, position_y)) # Items 是材质包

def draw_all(screen):        # 绘制全部对象
    draw_base_lines(screen)  # 绘制网格线
    draw_items(screen)       # 绘制地图上的物品
    show_position(screen)    # 左上角显示玩家坐标
    draw_main_player(screen) # 绘制玩家

# ! 需要将这个接口赋值成绘制背景图像的算法
draw_background = lambda screen: (draw_all(screen))

# ! 需要将这个接口赋值成事件处理工具
event_processor = lambda event: (set_event_check(event),)

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
            draw_background(self.screen)
            pygame.display.flip() # 更新显示窗口内容

if __name__ == "__main__":
    game = Game()
    game.run_game()
