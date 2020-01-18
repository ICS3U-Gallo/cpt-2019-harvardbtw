
import settings
import arcade
import random
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Zombie Smasher"

def anglefinder(x1, x2, y1, y2):
    x = x2 - x1
    y = y2 - y1

    rad = math.atan2(y, x)
    deg = math.degrees(rad)
    return deg

def mover(angle, spd, x, y):
    x += math.cos(math.radians(angle)) * spd
    y += math.sin(math.radians(angle)) * spd

    return x, y

def filter(exception, value):
    if exception != value:
        return value

class Zombie:
    def __init__(self, x, y, evolution, original_x, original_y, attack_ani_scale):

        #location and movement
        self.x = x
        self.y = y
        self.evolution = evolution
        self.original_x = original_x
        self.original_y = original_y
        self.scale = attack_ani_scale
        self.angle = 0
        self.spd = 0
        self.gb = False
        self.aal = 'Down'
        self.acl = 'Up'
        self.true_spd = 0
        self.end_loc_1 = 200

        #health
        self.hp_loc = original_x
        self.health = 15
        self.hp_backwards_by = 0
        self.healthheight = self.original_y + SCREEN_HEIGHT/3

        #time
        self.time_bool = False
        self.time_resetter = False
        self.time = 0
        self.time_thread2 = 0
        self.time_bool2 = 0
        self.time_resetter2 = 0

        #counters, attacks, etc.
        self.combo_counter = 0
        self.attack_choice = 0
        self.attack_order = [False, False, False]

        #rapid on-off and ordinary toggles
        self.toggle_dmg_box_spawn = False
        self.toggle_fade = False

        #spritelist and images
        self.boltlist = arcade.SpriteList(use_spatial_hash=False)
        self.zombie_sprite_1 = arcade.Sprite('Chapter4_Images/ZombLVL1.png', 1)
        self.zombie_sprite_2 = arcade.Sprite('Chapter4_Images/ZombLVL2.png', 1)
        self.zombie_sprite_3 = arcade.Sprite('Chapter4_Images/ZombLVL3.png', 1)

    def time_start(self, time_interval):
        if self.time_bool2 is True:
            self.time_thread2  += time_interval
        if self.time_resetter2 is True:
            self.time_thread2 = 0
            self.time_resetter2 = False
            self.time_bool2 = False
        if self.time_bool is True:
            self.time += time_interval
        if self.time_resetter is True:
            self.time = 0
            self.time_resetter = False
            self.time_bool = False

    def display_health(self):
        arcade.draw_rectangle_filled(self.hp_loc, self.healthheight, self.health*20, 25, (255, 0, 0))
        arcade.draw_rectangle_outline(self.original_x, self.healthheight, 300, 25, (0, 0, 0))

    def logic_health(self, hit):

        if hit is True and self.health != 0 and self.time_thread2 == 0:
            self.time_bool2 = True
            if self.evolution == 1:
                self.health -= 3
                self.hp_backwards_by = 3
            if self.evolution == 2:
                self.health -= 2
                self.hp_backwards_by = 2
            if self.evolution == 3:
                self.health -= 1
                self.hp_backwards_by = 1
            self.hp_loc += self.hp_backwards_by * 10
        if self.health <= 0:
            self.health = 15
            self.hp_loc = self.original_x
            self.evolution += 1
        if self.time_thread2 > 0.5:
            self.time_resetter2 = True

    def display_zm(self):
        if self.evolution == 1:
            self.zombie_sprite_1.draw()
            self.zombie_sprite_1.set_position(self.x, self.y)
        if self.evolution == 2:
            self.zombie_sprite_2.draw()
            self.zombie_sprite_2.set_position(self.x, self.y)
        if self.evolution == 3:
            self.zombie_sprite_3.draw()
            self.zombie_sprite_3.set_position(self.x, self.y)

    def move_zm(self, time_interval, evolution):

        if self.time == 0 and self.x == self.original_x and self.y == self.original_y:
            self.time_bool = True
            self.evolution = evolution

        pullback_x = self.original_x + self.scale
        pullback_x2 = self.original_x - self.scale
        pullback_y1 = self.original_y + self.scale
        pullback_y2 = self.original_y - self.scale

        og_spd = 600 * time_interval
        pulling_spd = 500 * time_interval
        if self.true_spd == 0:
            self.true_spd = og_spd

        if self.time >= 1:
            self.x = mover(self.angle, self.spd, self.x, self.y)[0]
            self.y = mover(self.angle, self.spd, self.x, self.y)[1]

        if self.time > 1 and any(self.attack_order) is False:
            if self.evolution == 1:
                self.attack_choice = random.randint(1, 3)
            if self.evolution == 2:
                self.attack_choice = random.randint(1, 5)
                if self.attack_choice == 5:
                    self.attack_choice = 4
            if self.evolution == 3:
                self.attack_choice = random.randint(1, 7)
                if self.attack_choice == 6:
                    self.attack_choice = 4
                if self.attack_choice == 7:
                    self.attack_choice = 5
            self.attack_order[0] = True
            self.spd = pulling_spd

        if self.time > 1 < 1.5:
            if self.attack_choice == 1 and self.attack_order[1] is False:
                if self.angle != 45:
                    self.angle = 45
                if self.y >= pullback_y1 and self.x >= pullback_x:
                    self.attack_order[1] = True
                    self.spd = 0
                    self.x = pullback_x
                    self.y = pullback_y1
            if self.attack_choice == 2 and self.attack_order[1] is False:
                if self.angle != 315:
                    self.angle = 315
                if self.y <= pullback_y1 and self.x >= pullback_x:
                    self.attack_order[1] = True
                    self.spd = 0
                    self.x = pullback_x
                    self.y = pullback_y2
            if self.attack_choice == 3 and self.attack_order[1] is False:
                if self.angle != 0:
                    self.angle = 0
                if self.x >= pullback_x:
                    self.attack_order[1] = True
                    self.spd = 0
                    self.x = pullback_x
            if self.evolution == 2 or self.evolution == 3:
                if self.attack_choice == 4 and self.attack_order[1] is False:
                    if self.angle != 135:
                        self.angle = 135
                    if self.y >= pullback_y1 and self.x <= pullback_x2:
                        self.attack_order[1] = True
                        self.spd = 0
                        self.x = pullback_x2
                        self.y = pullback_y1
            if self.evolution == 3:
                if self.attack_choice == 5 and self.attack_order[1] is False:
                    if self.angle != 225:
                        self.angle = 225
                    if self.y <= pullback_y2 and self.x <= pullback_x2:
                        self.attack_order[1] = True
                        self.spd = 0
                        self.x = pullback_x2
                        self.y = pullback_y2

        if self.time > 1.5 < 2.5 and self.attack_order[0] is True and self.attack_order[1] is True and self.attack_order[2] is False and self.attack_choice != 5:
            if self.attack_choice != 4:
                self.true_spd += 1.5
                self.spd = self.true_spd
                if self.angle != 180:
                    self.angle = 180
                if self.x <= self.end_loc_1:
                    self.x = self.end_loc_1
                    self.spd = 0
                    self.toggle_dmg_box_spawn = True
                    self.attack_order[2] = True
                    self.toggle_fade = True
            if self.evolution == 3 or self.evolution == 2:
                if self.attack_choice == 4:
                    self.true_spd += 1.75
                    self.spd = self.true_spd
                    if self.aal == 'Down':
                        if self.angle != anglefinder(self.x, self.end_loc_1, self.y, self.original_y - self.scale):
                            self.angle = anglefinder(self.x, self.end_loc_1, self.y, self.original_y - self.scale)
                        if self.x <= self.end_loc_1 and self.y <= self.original_y - self.scale:
                            self.x = self.end_loc_1
                            self.y = self.original_y - self.scale
                            self.spd = 0
                            self.aal = 'Up'
                            self.attack_order[2] = True
                            self.toggle_dmg_box_spawn = True
                            self.toggle_fade = True
                    elif self.aal == 'Up':
                        if self.angle != 180:
                            self.angle = 180
                        if self.x <= self.end_loc_1:
                            self.x = self.end_loc_1
                            self.spd = 0
                            self.aal = 'Down'
                            self.attack_order[2] = True
                            self.toggle_dmg_box_spawn = True
                            self.toggle_fade = True

        if self.evolution == 3:
            if self.attack_choice == 5 and self.time >= 1.5 and self.attack_order[2] is False:
                self.time = 1.5
                if self.x <= self.end_loc_1:
                    self.x = self.end_loc_1
                    self.toggle_fade = True
                    self.toggle_dmg_box_spawn = True
                    if self.acl == 'Up':
                        self.y = self.original_y + self.scale
                        self.acl = 'Medium'
                        self.combo_counter += 1
                    elif self.acl == 'Medium':
                        self.y = self.original_y
                        self.acl = 'Down'
                        self.combo_counter += 1
                    elif self.acl == 'Down':
                        self.y = self.original_y - self.scale
                        self.acl = 'Up'
                        self.combo_counter += 1
                    if self.angle != anglefinder(self.end_loc_1, self.original_x - self.scale, self.y, self.original_y - self.scale):
                        self.angle = anglefinder(self.end_loc_1, self.original_x - self.scale, self.y, self.original_y - self.scale)
                    if self.spd != og_spd * 2:
                        self.spd = og_spd * 2
                    if self.combo_counter == 3:
                        self.attack_order[2] = True
                        self.combo_counter = 0
                        self.time = 2.51
                        if self.acl == 'Up':
                            self.acl = 'Medium'
                        elif self.acl == 'Medium':
                            self.acl = 'Down'
                        elif self.acl == 'Down':
                            self.acl = 'Up'
                if self.x >= self.original_x - self.scale:
                    self.true_spd = og_spd
                    self.x = pullback_x2
                    self.y = pullback_y2
                    if self.acl == 'Up':
                        if self.angle != anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y + self.scale):
                            self.angle = anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y + self.scale)
                    if self.acl == 'Medium':
                        if self.angle != anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y):
                            self.angle = anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y)
                    if self.acl == 'Down':
                        if self.angle != anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y - self.scale):
                            self.angle = anglefinder(self.original_x - self.scale, self.end_loc_1, self.original_y - self.scale, self.original_y - self.scale)
                if self.angle > 90 < 270:
                    self.true_spd += 1.25
                    self.spd = self.true_spd

        if all(self.attack_order) is True and self.time > 2.5:
            self.gb = True

        if self.gb is True:
            if self.angle != anglefinder(self.x, self.original_x, self.y, self.original_y):
                self.angle = anglefinder(self.x, self.original_x, self.y, self.original_y)
            if self.spd != og_spd * 2:
                self.spd = og_spd * 2
            if self.x >= self.original_x:
                self.x = self.original_x
                self.y = self.original_y
                self.true_spd = 0
                self.spd = 0
                self.angle = 0
                self.gb = False
                self.time_resetter = True
                self.attack_order[0] = False
                self.attack_order[1] = False
                self.attack_order[2] = False

    def attack_territory_display(self):

        attack_1_hit = [[self.end_loc_1, self.original_y + self.scale], [self.end_loc_1, self.original_y], [self.end_loc_1 - self.scale, self.original_y]]
        attack_2_hit = [[self.end_loc_1, self.original_y - self.scale], [self.end_loc_1, self.original_y], [self.end_loc_1 - self.scale, self.original_y]]
        attack_3_hit = [[self.end_loc_1, self.original_y], [self.end_loc_1, self.original_y + self.scale], [self.end_loc_1, self.original_y - self.scale]]
        attack_list = [attack_1_hit, attack_2_hit, attack_3_hit]

        for i in range(len(attack_list)):
            if self.x == attack_list[i][0][0] and self.y == attack_list[i][0][1] and self.toggle_dmg_box_spawn == True:
                for i2 in range(len(attack_list[i])):
                    self.boltsprite = arcade.Sprite('Chapter4_Images/Damage_Marker.png')
                    self.boltsprite.center_x = attack_list[i][i2][0]
                    self.boltsprite.center_y = attack_list[i][i2][1]
                    self.boltlist.append(self.boltsprite)
                self.toggle_dmg_box_spawn = False

    def attack_territory_fade(self):
        if self.toggle_fade is True:
            self.boltlist.draw()
            for i in self.boltlist:
                if i.alpha >= 5:
                    i.alpha -= 5
        for i in self.boltlist:
            if i.alpha <= 5:
                self.boltlist.remove(i)
                self.toggle_fade = False


class Player:
    def __init__(self, x, y, movedist, original_x, forwards_x):

        self.x = x
        self.y = y
        self.movedist = movedist
        self.original_y = SCREEN_HEIGHT / 2
        self.original_x = original_x
        self.up_y = self.original_y + self.movedist
        self.down_y = self.original_y - self.movedist
        self.back_x = self.original_x - self.movedist
        self.forwards_x = forwards_x

        self.health = 15
        self.hp_backwards_by = 0
        self.hp_loc = self.original_x

        self.time = 0
        self.time_bool = False
        self.time_resetter = False

        self.player_image = arcade.Sprite('Chapter4_Images/Hero.png', 1)

    def time_start(self, time_interval):
        if self.time_bool is True:
            self.time += time_interval
        if self.time_resetter is True:
            self.time = 0
            self.time_resetter = False
            self.time_bool = False

    def logic_health(self, hit, evolution):

        if hit is True and self.health != 0:
            if evolution == 3:
                self.health -= 5
                self.hp_backwards_by = 5
            elif evolution == 2:
                self.health -= 3
                self.hp_backwards_by = 3
            elif evolution == 1:
                self.health -= 2
                self.hp_backwards_by = 2
            self.hp_loc -= self.hp_backwards_by*10

    def display_health(self):
        arcade.draw_rectangle_filled(self.hp_loc, self.original_y + SCREEN_HEIGHT/3, self.health*20, 25, (255, 0, 0))
        arcade.draw_rectangle_outline(self.original_x, self.original_y + SCREEN_HEIGHT/3, 300, 25, (0, 0, 0))

    def move(self, movements, time_interval):

        movement_speed = 800 * time_interval

        if movements[0] is True and movements[1] is False and movements[2] is False and movements[3] is False:
            if self.y <= self.up_y and self.time_bool is False:
                self.y += movement_speed
                if self.y > self.up_y:
                    self.y = self.up_y
                    self.time_bool = True
            if self.y > self.original_y and self.time > 0.3:
                self.y -= movement_speed
                if self.y < self.original_y:
                    self.y = self.original_y
                    self.time_resetter = True
                    movements[0] = False

        if movements[0] is False and movements[1] is True and movements[2] is False and movements[3] is False:
            if self.x >= self.back_x and self.time_bool is False:
                self.x -= movement_speed
                if self.x < self.back_x:
                    self.x = self.back_x
                    self.time_bool = True
            if self.x < self.original_x and self.time > 0.3:
                self.x += movement_speed
                if self.x > self.original_x:
                    self.x = self.original_x
                    self.time_resetter = True
                    movements[1] = False

        if movements[0] is False and movements[1] is False and movements[2] is True and movements[3] is False:
            if self.y >= self.down_y and self.time_bool is False:
                self.y -= movement_speed
                if self.y < self.down_y:
                    self.y = self.down_y
                    self.time_bool = True
            if self.y < self.original_y and self.time > 0.3:
                self.y += movement_speed
                if self.y > self.original_y:
                    self.y = self.original_y
                    self.time_resetter = True
                    movements[2] = False

        if movements[0] is False and movements[1] is False and movements[2] is False and movements[3] is True:
            if self.x <= self.forwards_x and self.time_bool is False:
                self.x += movement_speed*5
                if self.x > self.forwards_x:
                    self.x = self.forwards_x
                    self.time_bool = True
            if self.x > self.original_x and self.time_bool is True:
                self.x -= movement_speed*5
                if self.x < self.original_x:
                    self.x = self.original_x
                    self.time_resetter = True
                    movements[3] = False

    def display_pl(self):
        self.player_image.draw()
        self.player_image.set_position(self.x, self.y)


class Chapter4View(arcade.View):
    def __init__(self):

        #pause
        self.paused = False

        #Screens and Backgrounds

        #FPS
        self.FPS = 0
        self.FPS_counter = 0
        self.second_checker = 0

        #player centered variables
        self.attack_ani_scale = 100
        self.x_return = 200
        self.y_return = SCREEN_HEIGHT / 2
        self.movements = [False, False, False, False]
        self.hit = False

        #zombie centered variables
        self.evolution = 1
        self.player_hit = False

        super().__init__()

        arcade.set_background_color((255, 255, 255))

        #entities:
        self.pl = Player(self.x_return, self.y_return, self.attack_ani_scale, 200, 1000)
        self.zm = Zombie(1000, SCREEN_HEIGHT/2, self.evolution, 1000, SCREEN_HEIGHT/2, 100)

    def on_key_press(self, symbol: int, modifiers: int):
        if any(self.movements) is False:
            if symbol == 97:
                self.movements[0] = True
            if symbol == 115:
                self.movements[1] = True
            if symbol == 100:
                self.movements[2] = True
            if symbol == 119:
                self.movements[3] = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 65307:
            self.paused = not self.paused
        if symbol == arcade.key.ENTER:
            self.director.next_view()

    def on_draw(self):
        arcade.start_render()

        self.background.draw()

        self.zm.attack_territory_fade()
        self.zm.display_zm()
        self.zm.display_health()

        self.pl.display_pl()
        self.pl.display_health()

    def on_update(self, delta_time: float):

        #FPS logic
        self.FPS_counter += 1
        self.second_checker += delta_time
        if self.second_checker >= 1:
            self.FPS = self.FPS_counter
            self.FPS_counter = 0
            self.second_checker = 0
            print(self.FPS)

        if self.paused is False and self.FPS >= 37:

            #player logic
            self.pl.time_start(delta_time)
            self.pl.move(self.movements, delta_time)
            for i in self.zm.boltlist:
                if i.center_x + 50 > self.pl.x and i.center_x - 50 < self.pl.x and i.center_y + 50 > self.pl.y and i.center_y - 50 < self.pl.y and i.alpha >= 247.5:
                    self.hit = True
                    self.pl.logic_health(self.hit, self.evolution)
            if self.hit is True:
                self.hit = False

            #zombie logic
            self.zm.time_start(delta_time)
            self.zm.move_zm(delta_time, self.evolution)
            self.zm.attack_territory_display()
            if self.movements[3] is True:
                if self.pl.x <= self.zm.original_x and self.zm.x == self.zm.original_x:
                    self.player_hit = True
                    self.zm.logic_health(self.player_hit)
            if self.player_hit is True:
                self.player_hit = False

            if self.evolution != self.zm.evolution:
                self.evolution = self.zm.evolution


if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.
    You can ignore this whole section. Keep it at the bottom
    of your code.
    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1 / 70)
    my_view = Chapter4View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
