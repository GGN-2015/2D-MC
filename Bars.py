import Config
import Items
import Method
import Player

def make_border(x: float):
    return (1 - Config.BORDER_MARGIN) * x + Config.BORDER_MARGIN # 当血条满的时候 x = 1

def draw_life_bar(screen): # 绘制血条和饥饿条
    x, y = Config.LEFT_BOTTOM
    x_health = x + Config.BAR_MARGIN
    y_health = y - (Config.BAR_MARGIN + Config.BAR_HEIGHT)
    x_food = x + Config.BAR_MARGIN
    y_food = y - 2 * (Config.BAR_MARGIN + Config.BAR_HEIGHT)
    health_rate = make_border(Player.hit_point / Config.HIT_POINT_MAX)
    food_rate = make_border(Player.food_point / Config.FOOD_POINT_MAX)
    # print((health_rate, food_rate))
    health_color = Method.average(Config.GREEN, Config.RED, health_rate)
    Items.draw_rect(
        screen, 
        (x_health, y_health), 
        (Config.BAR_WIDTH * health_rate, Config.BAR_HEIGHT), 
        health_color
    ) # 绘制渐变色血量矩形
    Items.show_text(screen, (x_health + Config.BAR_WIDTH * health_rate + Config.BAR_MARGIN, y_health - Config.BAR_MARGIN), str(Player.hit_point), health_color)
    Items.draw_rect(
        screen, 
        (x_food, y_food), 
        (Config.BAR_WIDTH * food_rate, Config.BAR_HEIGHT), 
        Config.GREY
    ) # 绘制饥饿程度矩形
    Items.show_text(screen, (x_food + Config.BAR_WIDTH * food_rate + Config.BAR_MARGIN, y_food - Config.BAR_MARGIN), str(Player.food_point), Config.BAR_HEIGHT)

def draw_ammo_bar(screen):
    x, y = Config.RIGHT_BOTTOM
    x_ammo = x - Config.BAR_MARGIN
    y_ammo = y - Config.BAR_MARGIN - Config.BAR_HEIGHT
    ammo_now = Player.amo_count[Player.weapon_list[Player.weapon_id_now]]
    if ammo_now < 0:
        ammo_rate = 1
        ammo_str = "Infinity"
    else:
        ammo_rate = 1 - 2 ** (- ammo_now / Config.MIDDLE_AMMO) # 对数下降
        ammo_str = str(ammo_now)
    bar_len = Config.BAR_WIDTH * ammo_rate
    ammo_color = Method.average(Config.GREEN, Config.RED, ammo_rate)
    Items.draw_rect(
        screen, 
        (x_ammo - bar_len, y_ammo), 
        (bar_len, Config.BAR_HEIGHT), 
        ammo_color
    ) # 绘制子弹数量
    Items.show_text(screen, 
        (x_ammo - bar_len - 2 * Config.BAR_MARGIN - len(ammo_str) * Config.MESSAGE_FONT_SIZE // 2, y_ammo - Config.BAR_MARGIN), 
        ammo_str, 
    ) # 显示子弹数

