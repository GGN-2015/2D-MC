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

