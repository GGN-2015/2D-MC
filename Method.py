import Config

def distance(pointA, pointB): # 计算两点之间的距离
    dx = pointA[0] - pointB[0]
    dy = pointA[1] - pointB[1]
    return (dx ** 2 + dy ** 2) ** 0.5

def length(vec): # 计算向量长度
    return distance(vec, (0, 0))

def normalize(vec): # 取单位向量
    vec_len = length(vec)
    if vec_len == 0:
        return (0, 0)
    return (vec[0]/vec_len, vec[1]/vec_len)

def vec_add(vecA, vecB):
    return (vecA[0] + vecB[0], vecA[1] + vecB[1])

def vec_sub(vecA, vecB):
    return (vecA[0] - vecB[0], vecA[1] - vecB[1])

def vec_mul(vec, p):
    return (vec[0] * p, vec[1] * p)

def round(p): # 四舍五入
    if p >= 0:
        return int(p + 0.5)
    else:
        return int(p - 0.5)

def get_block_xy(x, y):
    return (round(x / Config.BLOCK_SIZE), round(y / Config.BLOCK_SIZE)) # 四舍五入找到最近的 block

def in_sight(pos_now, pos_player, dxdy, safe_span = 100): # 检查一个物品是否在玩家的视线范围内，也就是是否需要在屏幕上显示
    px, py = pos_now
    nx, ny = pos_player
    dx, dy = dxdy
    dx += safe_span
    dy += safe_span # 从屏幕外的一段距离就开始加载，放置突然闪入的情况
    xmin = nx - dx # xmin, xmax, ymin, ymax 是玩家可见的矩形区域
    xmax = nx + dx
    ymin = ny - dy
    ymax = ny + dy
    return xmin <= px and px <= xmax and ymin <= py and py <= ymax

def get_screen_pos(pos_xy, player_xy): # 将地图坐标映射到屏幕坐标
    block_x, block_y = pos_xy
    pos_x, pos_y = player_xy
    o_x, o_y = pos_x - Config.SCREEN_SIZE[0] // 2, pos_y - Config.SCREEN_SIZE[1] // 2
    vec = vec_sub((block_x, block_y), (o_x, o_y)) # 得到相对于左上角的坐标
    return vec

def get_pos_in_map(pos_on_screen, player_xy):   # 根据屏幕上的坐标计算玩家的坐标
    dW = Config.SCREEN_SIZE[0] // 2
    dH = Config.SCREEN_SIZE[1] // 2             # 玩家在屏幕上的位置
    vec = vec_sub(pos_on_screen, (dW, dH))      # 相对玩家的位移
    return vec_add(player_xy, vec)              # 得到游戏地图中的坐标

def circle_crash(pos1, R1, pos2, R2):
    return distance(pos1, pos2) <= R1 + R2 # 两个圆有相交部分

def not_in_screen(pos_xy, player_xy, R = 50): # 判断点在不在屏幕上
    pos = get_screen_pos(pos_xy, player_xy)
    dW = Config.SCREEN_SIZE[0] // 2 + R
    dH = Config.SCREEN_SIZE[1] // 2 + R # R 是对生物半径的修正
    return abs(pos[0] - dW) > dW and abs(pos[1] - dH) > dH

def average(lis1, lis2, alpha = 0.5):
    newlis = []
    for i in range(0, len(lis1)):
        newlis.append(lis1[i] * alpha + lis2[i] * (1-alpha))
    return tuple(newlis) # 将 list 打包成元组