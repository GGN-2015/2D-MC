import time

import Config
import Map
import Method

amo_count = {
    "WEAPON_PISTOL": -1, # < 0 表示无限子弹
    "WEAPON_AK47": 500
}

weapon_list = ["WEAPON_PISTOL", "WEAPON_AK47"]
on_fire = False # 正在射击

position_x = 0
position_y = 0 # 记录玩家所在的位置
color_of_main = Config.BLUE # 主人公的颜色

last_fire_time = time.time() # 上次开枪的时间
# weapon_now = "WEAPON_PISTOL" # 当前使用的武器
weapon_id_now = 0

player_score = 0
time_score = 0

last_score_time = time.time()

def get_score():
    global last_score_time # 计算上一次得秒数分的时间
    global time_score
    if not Config.PAUSED and Config.GAME_RUNNING:
        if time.time() - last_score_time >= 1:
            last_score_time = time.time()
            time_score += 10
    else:
        last_score_time = time.time()
    return time_score + player_score

hit_point = Config.HIT_POINT_MAX # 生命值
food_point = Config.FOOD_POINT_MAX # 饥饿度，food_point = 0 时开始掉生命值

last_eat_food = time.time()
last_damage = time.time()

def damage(cnt = 1):
    global last_damage
    global hit_point
    global food_point
    if time.time() - last_damage > Config.DAMAGE_SPAN and hit_point > 0:
        if food_point >= cnt: # 掉血优先掉饥饿值
            food_point -= cnt
        else:
            food_point = 0
            hit_point = max(hit_point - cnt, 0)
        last_damage = time.time()
    if hit_point <= 0:
        Config.GAME_RUNNING = False # you died
        Config.GAME_OVER_TIME = time.time()

def player_around_aid_box(): # 检测周围有没有 aid_box
    global amo_count
    global food_point
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    bx, by = Method.get_block_xy(*get_position())
    for dx, dy in dirs:
        nx = bx + dx
        ny = by + dy
        if Map.map_of_objects.get((nx, ny)) == "ITEM_AID_BOX":
            Map.map_of_objects[(nx, ny)] = "ITEM_USED_AID_BOX"
            amo_count["WEAPON_AK47"] += 200
            food_point = Config.FOOD_POINT_MAX # 直接吃饱了
    pass

def check_food_point_change():
    global food_point
    global hit_point
    global last_eat_food
    if time.time() - last_eat_food >= Config.FOOD_TIME_SPAN:
        last_eat_food = time.time()
        if food_point > 0:
            food_point -= 1
        else:
            if hit_point > 0:
                hit_point -= 1
            else:
                # print("You die of hunger.")
                Config.GAME_RUNNING = False
                Config.GAME_OVER_TIME = time.time()



def get_message(): # 获得玩家消息字符串
    global amo_count
    POS = "Position: (%d, %d)\n" % Method.get_block_xy(position_x, position_y)
    TIM = "Time: %s\n" % Method.get_game_time()
    WPN = "Weapon: %s\n" % get_weapon_name()
    SCO = "Score: %d\n" % get_score()
    # if amo_count[get_weapon_name()] >= 0:
    #     AMO = "amo: %d\n" % amo_count[get_weapon_name()]
    # else:
    #     AMO = "amo: infinity\n"
    # HP = "HitPoint: %d\n" % hit_point
    # FP = "FoodPoint: %d\n" % food_point
    return POS + TIM + WPN + SCO # + AMO + HP + FP

def get_position():
    return (position_x, position_y) # 反馈位置信息

def get_weapon_name():
    return weapon_list[weapon_id_now]

def next_weapon(): # 切换到下一把武器
    global weapon_id_now
    weapon_id_now += 1
    weapon_id_now %= len(weapon_list)