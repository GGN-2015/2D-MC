# 材质包
import pygame

import Config
import Method

def draw_item_box(screen, block_xy, position_xy): # 绘制一个箱子
    block_x, block_y = Method.vec_mul(block_xy, Config.BLOCK_SIZE) # 找到几何中心坐标
    pos_x, pos_y = position_xy
    o_x, o_y = pos_x - Config.SCREEN_SIZE[0] // 2, pos_y - Config.SCREEN_SIZE[1] // 2
    vec = Method.vec_sub((block_x, block_y), (o_x, o_y)) # 得到相对于左上角的坐标
    R = Config.BLOCK_SIZE // 2
    pygame.draw.rect(screen, (0xde, 0xcb, 0x0e), (vec[0] - R, vec[1] - R, 2*R, 2*R))
    pygame.draw.rect(screen, Config.BORDER_WIDTH, (vec[0] - R, vec[1] - R, 2*R, 2*R), width = Config.LINE_WIDTH)


get_draw_method = { # 确定每种物品的绘图函数
    "ITEM_BOX" : draw_item_box
}

def draw_item(screen, item_type, block_xy, position_xy):
    if get_draw_method.get(item_type) != None:
        draw_method = get_draw_method[item_type]
    else:
        draw_method = draw_undefine
    draw_method(screen, block_xy, position_xy) # 根据找到的函数进行绘制
