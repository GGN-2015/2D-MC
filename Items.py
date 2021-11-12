# 材质包文件 Items.py
# 对材质包进行修改不会造成游戏本质的改变

import pygame

import Config
import Method

def show_text(screen, screen_xy, message_str: str, text_color = Config.MESSAGE_COLOR):
    font = pygame.font.SysFont(Config.MESSAGE_FONT_NAME, Config.MESSAGE_FONT_SIZE) # 使用系统字体
    text = font.render(message_str, True, text_color)
    screen.blit(text, screen_xy)

def draw_amo(screen, amo_pos, player_pos):
    vec = Method.get_screen_pos(amo_pos, player_pos) # 从地图坐标映射到平面坐标
    pygame.draw.circle(screen, Config.AMO_COLOR, (vec[0], vec[1]), Config.AMO_R, width = Config.AMO_LINE_WIDTH)

def draw_item_base(screen, block_xy, player_xy, border_color, box_color): # 绘制一个物品的基础算法
    block_x, block_y = Method.vec_mul(block_xy, Config.BLOCK_SIZE) # 找到几何中心坐标
    vec = Method.get_screen_pos((block_x, block_y), player_xy) # 计算得到屏幕上某点的位置
    R = Config.BLOCK_SIZE // 2
    pygame.draw.rect(screen, box_color, (vec[0] - R, vec[1] - R, 2*R, 2*R))
    pygame.draw.rect(screen, border_color, (vec[0] - R, vec[1] - R, 2*R, 2*R), width = Config.LINE_WIDTH)

def draw_item_block(screen, block_xy, player_xy): # 绘制一个路障
    draw_item_base(screen, block_xy, player_xy, Config.BORDER_COLOR, (0xde, 0xcb, 0x0e))

def draw_item_aid_box(screen, block_xy, player_xy): # 绘制一个箱子
    draw_item_base(screen, block_xy, player_xy, Config.BORDER_COLOR, Config.GREEN) # 绿色代表健康

def draw_item_used_aid_box(screen, block_xy, player_xy): # 绘制一个用过的箱子
    draw_item_base(screen, block_xy, player_xy, Config.BORDER_COLOR, Config.GREY) # 灰色代表不健康
    
def draw_undefine(screen, block_xy, player_xy): # 绘制一个未知方块的算法
    draw_item_base(screen, block_xy, player_xy, Config.BORDER_COLOR, Config.UNKNOW_COLOR)

get_draw_method = { # 确定每种物品的绘图函数
    "ITEM_BLOCK" : draw_item_block,
    "ITEM_AID_BOX": draw_item_aid_box,
    "ITEM_USED_AID_BOX": draw_item_used_aid_box
}

def draw_item(screen, item_type, block_xy, player_xy):
    if get_draw_method.get(item_type) != None:
        draw_method = get_draw_method[item_type]
    else:
        draw_method = draw_undefine
    draw_method(screen, block_xy, player_xy) # 根据找到的函数进行绘制

def draw_rect(screen, screen_xy, width_xy, color, width = 0): # 绘制实心矩形
    pygame.draw.rect(screen, color, (screen_xy[0], screen_xy[1], width_xy[0], width_xy[1]), width)
