import time

SCREEN_SIZE = (800, 600)
GAME_NAME = "Survivor"

BLOCK_SIZE = 50 # 一个网格的大小

ROW_BLOCK_CNT = 16
COLUMN_BLOCK_CNT = 12 # 记录每一行和每一列的元素个数

WHITE = (255, 255, 255)
GREEN = (0x00, 0x80, 0x00)
GREY = (127, 127, 127)

BACKGROUND_COLOR = WHITE # 默认白色
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

BEGIN_TIME = time.time()

def MONSTER_SPEED():
    return (time.time() - BEGIN_TIME) / 60 * MONSTER_ACCELERATION + MONSTER_BASIC_SPEED

MONSTER_R = {
    "MONSTER_ZOMBIE": BLOCK_SIZE // 2 # 普通僵尸的半径
}
HIT_BACK = 1 # 击退效果系数
MONSTER_MAX = 100 # 地图中最多有 100 个怪物
MONSTER_LINE_WIDTH = PLAYER_LINE_WIDTH

MONSTER_COLOR = (200, 200, 200) # 深灰色
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

FOOD_TIME_SPAN = 3 # 每 3s 减一点 food_point
FOOD_POINT_MAX = 100 # 初始食物点数
HIT_POINT_MAX = 100

GAME_RUNNING = True # 游戏仍在继续进行
POSITION_EPS = 10 # 10 bit position

DAMAGE_SPAN = 0.07 # 每 0.07 秒 掉一滴血
GAME_OVER_TIME = None