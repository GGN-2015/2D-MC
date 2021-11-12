import time

SCREEN_SIZE = (800, 600)
GAME_NAME = "Survivor"

BLOCK_SIZE = 50 # 一个网格的大小

ROW_BLOCK_CNT = 16
COLUMN_BLOCK_CNT = 12 # 记录每一行和每一列的元素个数

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0x00, 0x80, 0x00)
LIGHT_GREY = (225, 225, 225)
GREY = (127, 127, 127)

RED = (0xFF, 0x00, 0x00)
LIGHT_GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0x80)

BACKGROUND_COLOR = LIGHT_GREY # 默认白色
LINE_COLOR = GREY # 默认灰色

LINE_WIDTH = 2 # 网格线宽度
BORDER_WIDTH = LINE_WIDTH

PLAYER_LINE_WIDTH = LINE_WIDTH * 3
PLAYER_R = BLOCK_SIZE // 2

SPEED = 0.4 * 2 # 玩家默认移动速度
AMO_SPEED = 10 * SPEED

MESSAGE_FONT_NAME = "microsoftyaheimicrosoftyaheiui" # 使用系统字体
MESSAGE_FONT_SIZE = 20
MESSAGE_COLOR = (0, 0, 0)

AMO_SPAN = {
    "WEAPON_PISTOL": 0.3, # 子弹能生存不超过 0.3 秒钟时间
    "WEAPON_AK47": 1 # 提高子弹的射程
}

BORDER_COLOR = (0, 0, 0)
UNKNOW_COLOR = (127, 127, 127)

AMO_R = 4               # 球型子弹的半径
AMO_LINE_WIDTH = 2      # 子弹小球边界宽度
AMO_COLOR = (0, 0, 0)   # 子弹小球的颜色
AMO_MAX = 30            # 屏幕上最多能够容纳的子弹个数

WEAPON_REFRESH_TIME = {
    "WEAPON_PISTOL": 0.3, # 手枪每 0.2 秒可以发射一发子弹
    "WEAPON_AK47": 0.07 # AK47
}

MESSAGE_HEIGHT = 25 # 每行消息的高度

MONSTER_BASIC_SPEED = 0.65 * SPEED  # 僵尸的默认移动速度
MONSTER_ACCELERATION = MONSTER_BASIC_SPEED * 0.15 # 僵尸每分钟的加速度
MONSTER_MAX_SPEED = 2.0 * SPEED # 僵尸的最大速度, <= 0 或者为 None 表示没有上界

MONSTER_SCORE = 100 # 打死一只僵尸的收益
SCORE_PER_SECOND = 10 # 存活一秒的收益

BEGIN_TIME = time.time()

def MONSTER_SPEED():
    """获取怪物当前的速度"""
    if MONSTER_MAX_SPEED == None or MONSTER_MAX_SPEED > 0:
        return min((time.time() - BEGIN_TIME) / 60 * MONSTER_ACCELERATION + MONSTER_BASIC_SPEED, MONSTER_MAX_SPEED)
    else:
        return (time.time() - BEGIN_TIME) / 60 * MONSTER_ACCELERATION + MONSTER_BASIC_SPEED

MONSTER_R = {
    "MONSTER_ZOMBIE": BLOCK_SIZE // 2 # 普通僵尸的半径
}

HIT_BACK = 1 # 击退效果系数
MONSTER_MAX = 100 # 地图中最多有 100 个怪物
MONSTER_LINE_WIDTH = PLAYER_LINE_WIDTH

MONSTER_COLOR = RED # 红色
MONSTER_SPAN = 0.5 # 每 0.5 秒生成一次僵尸
MONSTER_OK = True # 记录当前是否可以生成僵尸
MONSTER_FADE_TIME = 1 # 僵尸死亡后显示的时间

AID_BOX_SPAN = 4 # 没 5 秒生成一个宝箱

MAX_SEARCH_DEPTH = 10 # 僵尸寻路的最大层数

DESTROYABLE = [
    "ITEM_BLOCK" # 可摧毁的路障
]

TRANSPARENT = [ # 透明方块

]

PASSABLE = [ # 课穿过方块

]

FOOD_TIME_SPAN = 2 # 每 2s 减一点 food_point
FOOD_POINT_MAX = 100 # 初始食物点数
HIT_POINT_MAX = 100

GAME_RUNNING = True # 游戏仍在继续进行
PAUSED = False # 游戏暂停状态
POSITION_EPS = 10 # 10 bit position

DAMAGE_SPAN = 0.05 # 每 0.05 秒 掉一滴血
GAME_OVER_TIME = None

BAR_WIDTH = 200
BAR_MARGIN = 5
BAR_HEIGHT = 20 # 血条与食物条相关的常量

LEFT_BOTTOM = (0, SCREEN_SIZE[1]) # 左下角的坐标
RIGHT_BOTTOM = SCREEN_SIZE

BORDER_MARGIN = 0.05 # 当血条为空时，显示的条带的长度
MIDDLE_AMMO = 600 # 当子弹条恰好一般的时候子弹的数量