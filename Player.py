import time

import Method

amo_count = {
    "WEAPON_PISTOL": -1, # < 0 表示无限子弹
    "WEAPON_AK47": 1000
}

weapon_list = ["WEAPON_PISTOL", "WEAPON_AK47"]
on_fire = False # 正在射击

position_x = 0
position_y = 0 # 记录玩家所在的位置
color_of_main = (255, 0, 0) # 主人公的颜色

last_fire_time = time.time() # 上次开枪的时间
# weapon_now = "WEAPON_PISTOL" # 当前使用的武器
weapon_id_now = 0

def get_message(): # 获得玩家消息字符串
    global amo_count
    POS = "Position: (%d, %d)\n" % Method.get_block_xy(position_x, position_y)
    WPN = "Weapon: %s\n" % get_weapon_name()
    if amo_count[get_weapon_name()] >= 0:
        AMO = "amo: %d\n" % amo_count[get_weapon_name()]
    else:
        AMO = "amo: infinity\n"
    return POS + WPN + AMO

def get_position():
    return (position_x, position_y) # 反馈位置信息

def get_weapon_name():
    return weapon_list[weapon_id_now]

def next_weapon(): # 切换到下一把武器
    global weapon_id_now
    weapon_id_now += 1
    weapon_id_now %= len(weapon_list)