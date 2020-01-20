
import arcade
import random
import math
from settings import HEIGHT, WIDTH

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
SCREEN_TITLE = "Zombie Smasher"

#finds angle between two points
def anglefinder(x1, x2, y1, y2):
    x = x2 - x1
    y = y2 - y1

    rad = math.atan2(y, x)
    deg = math.degrees(rad)
    return deg

#finds new x and y position based on spd, angle, and the old x and y position
def mover(angle, spd, x, y):
    x += math.cos(math.radians(angle)) * spd
    y += math.sin(math.radians(angle)) * spd

    return x, y

def filter(exception, value):
    if exception != value:
        return value

class Zombie:
    def __init__(self, evolution, player_dodge_scale):
        #location and movement
        self.x = SCREEN_WIDTH*(4/5)
        self.y = SCREEN_HEIGHT/2
        self.evolution = evolution
        self.original_x = SCREEN_WIDTH*(4/5)
        self.original_y = SCREEN_HEIGHT/2
        self.scale = player_dodge_scale
        self.angle = 0
        self.spd = 0
        self.gb = False
        self.aal = 'Down'
        self.acl = 'Up'
        self.true_spd = 0
        self.end_loc_1 = WIDTH/5
        self.og_spd_base = 500
        self.pulling_spd_base = 400

        #health
        self.hp_loc = self.original_x
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
        self.attack_bool = False

        #rapid on-off and ordinary toggles
        self.toggle_dmg_box_spawn = False
        self.toggle_fade = False

        #spritelist and images
        self.boltlist = arcade.SpriteList(use_spatial_hash=False)
        self.zombie_sprite_1 = arcade.Sprite('Chapter4_Images/ZombLVL1.png', 0.75)
        self.zombie_sprite_2 = arcade.Sprite('Chapter4_Images/ZombLVL2.png', 0.75)
        self.zombie_sprite_3 = arcade.Sprite('Chapter4_Images/ZombLVL3.png', 0.75)

    def restart(self):
        #same thing as the restart function in the player class, but for this one
        self.health = 15
        self.hp_backwards_by = 0
        self.hp_loc = self.original_x

        self.evolution = 1

        self.attack_order = [False, False, False]
        self.toggle_fade = False
        for i in self.boltlist:
             self.boltlist.remove(i)

        self.x = self.original_x
        self.y = self.original_y

        self.time_resetter2 = True
        self.time_resetter = True

    def time_start(self, time_interval):
        #the zombie's personal 'clocks'
        if self.time_bool2 is True:
            self.time_thread2 += time_interval
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
        #displays zombie health
        arcade.draw_rectangle_filled(self.hp_loc, self.healthheight, self.health*20, 25, (255, 0, 0))
        arcade.draw_rectangle_outline(self.original_x, self.healthheight, 300, 25, (0, 0, 0))

    def logic_health(self, hit, player_x, devmode):

        #logic behind the health of the zombie
        if player_x >= self.original_x - self.scale and self.x == self.original_x:
            hit = True
        if hit is True and self.time_thread2 == 0 and self.health > 0:
            self.time_bool2 = True
            if self.evolution == 1:
                self.health -= 3
                self.hp_backwards_by = 3
            if self.evolution == 2:
                self.health -= 1
                self.hp_backwards_by = 1
            if self.evolution == 3:
                self.health -= 0.75
                self.hp_backwards_by = 0.75
            if devmode is True:
                self.health -= 5
            self.hp_loc += self.hp_backwards_by * 10
        if self.time_thread2 > 0.5 and self.health > 0:
            self.time_resetter2 = True
        if self.health <= 0:
            self.health = 0
            if self.time_bool2 is False:
                self.time_bool2 = True
            if self.time_thread2 > 3:
                self.health = 15
                self.hp_loc = self.original_x
                self.evolution += 1
                self.time_resetter2 = True
                self.time_resetter = True
                self.x = self.original_x
                self.y = self.original_y

    def display_zm(self):
        #displays the zombie sprites depending on evolution
        if self.evolution == 1:
            self.zombie_sprite_1.draw()
            self.zombie_sprite_1.set_position(self.x, self.y)
        if self.evolution == 2:
            self.zombie_sprite_2.draw()
            self.zombie_sprite_2.set_position(self.x, self.y)
        if self.evolution == 3:
            self.zombie_sprite_3.draw()
            self.zombie_sprite_3.set_position(self.x, self.y)
        if self.health == 0:
            self.zombie_sprite_1.angle = 90
            self.zombie_sprite_2.angle = 90
            self.zombie_sprite_3.angle = 90
        if self.health > 0 and self.zombie_sprite_1.angle != 0:
            self.zombie_sprite_1.angle = 0
            self.zombie_sprite_2.angle = 0
            self.zombie_sprite_3.angle = 0

    def move_zm(self, time_interval):

        #determines when everything should be 'reset', and boots the entire 'attack process' up when it should be
        if self.time == 0 and self.x == self.original_x and self.y == self.original_y:
            self.time_bool = True
            if self.evolution == 2 or self.evolution == 3:
                self.time = 0.5
        #determines whether the zombie is attacking or not (for other code)
        if self.angle > 90 < 270 and self.spd > 0:
            self.attack_bool = True
        else:
            self.attack_bool = False

        if self.health > 0:
            #defines all the spds (pulling, which is how fast the zombie moves while preparing for an attack, and og spd, the benchmark of truespd), and the coords which the zombie should aim to pullback to
            pullback_x = self.original_x + self.scale
            pullback_x2 = self.original_x - self.scale
            pullback_y1 = self.original_y + self.scale
            pullback_y2 = self.original_y - self.scale

            og_spd = self.og_spd_base * time_interval
            pulling_spd = self.pulling_spd_base * time_interval

            if self.true_spd == 0:
                #returns true spd to og_spd upon being set to zero by the attacks
                self.true_spd = og_spd

            if self.time >= 1:
                #code that actually moves the zombie depending on angle, spd, and previous x and y position
                self.x = mover(self.angle, self.spd, self.x, self.y)[0]
                self.y = mover(self.angle, self.spd, self.x, self.y)[1]

            if self.time > 1 and any(self.attack_order) is False:
                #code that defines how the zombie chooses its attack
                if self.evolution == 1:
                    self.attack_choice = random.randint(1, 3)
                if self.evolution == 2:
                    self.attack_choice = random.randint(1, 5)
                    if self.attack_choice == 5:
                        self.attack_choice = 4
                if self.evolution == 3:
                    self.attack_choice = random.randint(1, 8)
                    if self.attack_choice == 6:
                        self.attack_choice = 4
                    if self.attack_choice == 7 or self.attack_choice == 8:
                        self.attack_choice = 5
                self.attack_order[0] = True
                self.spd = pulling_spd

            if self.time > 1 < 1.5:
                #code which defines the zombie's 'attack preparation phase'
                if self.attack_choice == 1 and self.attack_order[1] is False:
                    self.angle = 45
                    if self.y >= pullback_y1 and self.x >= pullback_x:
                        self.attack_order[1] = True
                        self.spd = 0
                        self.x = pullback_x
                        self.y = pullback_y1
                if self.attack_choice == 2 and self.attack_order[1] is False:
                    self.angle = 315
                    if self.y <= pullback_y1 and self.x >= pullback_x:
                        self.attack_order[1] = True
                        self.spd = 0
                        self.x = pullback_x
                        self.y = pullback_y2
                if self.attack_choice == 3 and self.attack_order[1] is False:
                    self.angle = 0
                    if self.x >= pullback_x:
                        self.attack_order[1] = True
                        self.spd = 0
                        self.x = pullback_x
                if self.evolution == 2 or self.evolution == 3:
                    if self.attack_choice == 4 and self.attack_order[1] is False:
                        self.angle = 135
                        if self.y >= pullback_y1 and self.x <= pullback_x2:
                            self.attack_order[1] = True
                            self.spd = 0
                            self.x = pullback_x2
                            self.y = pullback_y1
                if self.evolution == 3:
                    if self.attack_choice == 5 and self.attack_order[1] is False:
                        self.angle = 225
                        if self.y <= pullback_y2 and self.x <= pullback_x2:
                            self.attack_order[1] = True
                            self.spd = 0
                            self.x = pullback_x2
                            self.y = pullback_y2

            if self.time > 1.5 < 2.5 and self.attack_order[0] is True and self.attack_order[1] is True and self.attack_order[2] is False and self.attack_choice != 5:
                #default first three attacks
                if self.attack_choice != 4:
                    self.true_spd += 1.5
                    self.spd = self.true_spd
                    self.angle = 180
                    if self.x <= self.end_loc_1:
                        self.x = self.end_loc_1
                        self.spd = 0
                        self.toggle_dmg_box_spawn = True
                        self.attack_order[2] = True
                #code behind the 2nd and 3rd zombies 'Northwest' attack
                if self.evolution == 3 or self.evolution == 2:
                    if self.attack_choice == 4:
                        self.true_spd += 1.75
                        self.spd = self.true_spd
                        if self.aal == 'Down':
                            self.angle = anglefinder(self.x, self.end_loc_1, self.y, self.original_y - self.scale)
                            if self.x <= self.end_loc_1 and self.y <= self.original_y - self.scale:
                                self.x = self.end_loc_1
                                self.y = self.original_y - self.scale
                                self.spd = 0
                                self.aal = 'Up'
                                self.attack_order[2] = True
                                self.toggle_dmg_box_spawn = True
                        elif self.aal == 'Up':
                            self.angle = 180
                            if self.x <= self.end_loc_1:
                                self.x = self.end_loc_1
                                self.spd = 0
                                self.aal = 'Down'
                                self.attack_order[2] = True
                                self.toggle_dmg_box_spawn = True

            #the code behind the 3rd evolution zombie's triple attack (Southeast attack)
            if self.evolution == 3:
                if self.attack_choice == 5 and self.time >= 1.5 and self.attack_order[2] is False:
                    self.time = 1.5
                    if self.x <= self.end_loc_1:
                        self.x = self.end_loc_1
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

            #this triggers the variable that triggers the zombie to return to its original position
            if all(self.attack_order) is True and self.time > 2.5:
                self.gb = True

            #code that allows zombie to return to original position
            if self.gb is True:
                self.angle = anglefinder(self.x, self.original_x, self.y, self.original_y)
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

        #code that spawns the diagonal lines
        attack_1_hit = [[self.end_loc_1, self.original_y + self.scale], [self.end_loc_1, self.original_y], [self.end_loc_1 - self.scale, self.original_y]]
        attack_2_hit = [[self.end_loc_1, self.original_y - self.scale], [self.end_loc_1, self.original_y], [self.end_loc_1 - self.scale, self.original_y]]
        attack_3_hit = [[self.end_loc_1, self.original_y], [self.end_loc_1, self.original_y + self.scale], [self.end_loc_1, self.original_y - self.scale]]
        attack_list = [attack_1_hit, attack_2_hit, attack_3_hit]

        for i in range(len(attack_list)):
            if self.x == attack_list[i][0][0] and self.y == attack_list[i][0][1] and self.toggle_dmg_box_spawn is True:
                for i2 in range(len(attack_list[i])):
                    self.boltsprite = arcade.Sprite('Chapter4_Images/Damage_Marker.png', self.scale/100)
                    self.boltsprite.center_x = attack_list[i][i2][0]
                    self.boltsprite.center_y = attack_list[i][i2][1]
                    self.boltlist.append(self.boltsprite)
                self.toggle_dmg_box_spawn = False
                self.toggle_fade = True

    def attack_territory_fade(self):

        #code behind the diagonal lines fading
        if self.toggle_fade is True:
            self.boltlist.draw()
            for i in self.boltlist:
                if i.alpha >= 5:
                    i.alpha -= 5
        for i in self.boltlist:
            if i.alpha <= 5:
                self.boltlist.remove(i)
        if len(self.boltlist) == 0:
            self.toggle_fade = False


class Player:
    def __init__(self, movedist):

        #movement and location
        self.x = SCREEN_WIDTH/5
        self.y = SCREEN_HEIGHT/2
        self.movedist = movedist
        self.original_y = self.y
        self.original_x = self.x
        self.movedist = movedist
        self.move_spd_base = 600

        self.up_y = self.original_y + self.movedist
        self.down_y = self.original_y - self.movedist
        self.back_x = self.original_x - self.movedist
        self.forwards_x = SCREEN_WIDTH*(4/5)

        #health
        self.health = 15
        self.hp_backwards_by = 0
        self.hp_loc = self.original_x
        self.gameover_bool = False

        #time
        self.time = 0
        self.time_bool = False
        self.time_resetter = False

        #images and sprites
        self.player_image = arcade.Sprite('Chapter4_Images/Hero.png', 0.75)

    def restart(self):
        #returns player to original state
        self.health = 15
        self.hp_backwards_by = 0
        self.hp_loc = self.original_x

        self.x = self.original_x
        self.y = self.original_y

    def time_start(self, time_interval):

        #the code for the player's 'personal clock'
        if self.time_bool is True:
            self.time += time_interval
        if self.time_resetter is True:
            self.time = 0
            self.time_resetter = False
            self.time_bool = False

    def logic_health(self, hit, evolution):

        #what happens upon hit
        if hit is True and self.health > 0:
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

        #what happens when health is at zero
        if self.health <= 0:
            self.gameover_bool = True

    def display_health(self):

        #code behind displaying the player health bar
        arcade.draw_rectangle_filled(self.hp_loc, self.original_y + SCREEN_HEIGHT/3, self.health*20, 25, (255, 0, 0))
        arcade.draw_rectangle_outline(self.original_x, self.original_y + SCREEN_HEIGHT/3, 300, 25, (0, 0, 0))

    def move(self, movements, time_interval):

        #constantly modifies the variable movement speed depending on the time in between each loop, and the base 'anchor' speed
        movement_speed = self.move_spd_base * time_interval

        #takes care of all logic based around player movements
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

        if movements[0] is False and movements[1] is False and movements[2] is False and movements[3]:
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
        #displays player
        self.player_image.draw()
        self.player_image.set_position(self.x, self.y)


class TextScreens:
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.level1text = arcade.Sprite('Chapter4_Images/TextZomb1.png', center_x=self.x, center_y=self.y)
        self.level2text = arcade.Sprite('Chapter4_Images/TextZomb2.png', center_x=self.x, center_y=self.y)
        self.level3text = arcade.Sprite('Chapter4_Images/TextZomb3.png', center_x=self.x, center_y=self.y)
        self.endtext = arcade.Sprite('Chapter4_Images/Endscreen.png', center_x=self.x, center_y=self.y)

    def display_text(self, screen_choice):
        #displays text depending on screenchoice
        if screen_choice == 1:
            self.level1text.draw()
        if screen_choice == 2:
            self.level2text.draw()
        if screen_choice == 3:
            self.level3text.draw()
        if screen_choice == 4:
            self.endtext.draw()

class Gameoverscreen:
    def __init__(self):
        self.width = SCREEN_WIDTH / 1.5
        self.height = SCREEN_HEIGHT / 1.5
        self.x = SCREEN_WIDTH/2
        self.chooser_x = self.x - (self.width/4)
        self.y = SCREEN_HEIGHT/2
        self.up_y = self.y - 50
        self.down_y = self.y - 100
        self.chooser_loc = 100

        self.bool_restart = False
        self.bool_restartallviews = False

    def display_gameover(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, (58, 58, 58))

        arcade.draw_text("Y O U  D I E D",
                         self.x, self.y, (255, 255, 255), 25, width=200, align="center", anchor_x='center')

        arcade.draw_text("R E S T A R T  V I E W",
                         self.x, self.y - 50, (255, 255, 255), 14, width=200, align="center", anchor_x='center')
        arcade.draw_text("D O  I T ,  R E S T A R T",
                         self.x, self.y - 100, (255, 255, 255), 14, width=200, align="center", anchor_x='center')
        arcade.draw_text(">",
                         self.chooser_x, self.y - self.chooser_loc, (255, 255, 255), 14, width=200)

    def gameover_logic(self, movements, enter):

        #code to choose between options
        if movements[0] is True and self.chooser_loc != 50:
            self.chooser_loc = 50
        if movements[1] is True and self.chooser_loc != 100:
            self.chooser_loc = 100
        if enter is True and self.chooser_loc == 50 or enter is True and self.chooser_loc == 100:
            self.bool_restart = True
            enter = False

        #switch all movement elements to 'false'
        if any(movements) is True:
            for i in movements:
                movements[i] = False

class Opening_screen:
    def __init__(self):

        #locations and movement
        self.x = SCREEN_HEIGHT/2
        self.y = SCREEN_HEIGHT/2

        #sprites, pictures, and images
        self.opening_screen = arcade.Sprite('Chapter4_Images/OpeningScreen.png', 0.8, center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT/2)

    def display_op(self):
        self.opening_screen.draw()


class Chapter4View(arcade.View):
    def __init__(self):

        #pause and other game states
        self.paused = False
        self.restart = False
        self.opening_screen_bool = True
        self.dev_mode = False

        #Screens and Backgrounds
        self.text_counter = 1
        self.text_boolean = True
        self.screen_movements = [False, False]

        #FPS
        self.FPS = 0
        self.FPS_counter = 0
        self.second_checker = 0

        #player centered variables
        self.attack_ani_scale = 75
        self.x_return = WIDTH/5
        self.y_return = SCREEN_HEIGHT/2
        self.movements = [False, False, False, False]
        self.hit = False
        self.gameover = False

        #zombie centered variables
        self.damage_areas = self.attack_ani_scale/2
        self.evolution = 1
        self.player_hit = False

        #gameover centered variable
        self.chooser_loc = 0
        self.enter = False

        super().__init__()

        arcade.set_background_color((255, 255, 255))

        #entities:
        self.pl = Player(self.attack_ani_scale)
        self.zm = Zombie(self.evolution, self.attack_ani_scale)
        self.textscreens = TextScreens()
        self.gameover_options = Gameoverscreen()
        self.opener = Opening_screen()

    def on_key_press(self, symbol: int, modifiers: int):
        #player movements
        if any(self.movements) is False:
            if symbol == 97:
                self.movements[0] = True
            if symbol == 115:
                self.movements[1] = True
            if symbol == 100:
                self.movements[2] = True
            if symbol == 119 and self.zm.attack_bool is False:
                self.movements[3] = True

    def on_key_release(self, symbol: int, modifiers: int):

        #general stuff (pausing, accepting text, etc.)
        if symbol == 65307:
            self.paused = not self.paused
        if symbol == 65293:
            self.enter = True

        #up down screen navigation
        if symbol == 65362:
            self.screen_movements[0] = True
        if symbol == 65364:
            self.screen_movements[1] = True

        #dev testing stuff
        if symbol == 65507:
            self.dev_mode = not self.dev_mode

        if self.dev_mode is True:
            if symbol == 49:
                self.zm.evolution = 1
            if symbol == 50:
                self.zm.evolution = 2
            if symbol == 51:
                self.zm.evolution = 3
            if symbol == 52:
                self.zm.evolution = 4

    def on_draw(self):
        arcade.start_render()

        if self.opening_screen_bool is True:

            #displays opening screen
            self.opener.display_op()
            if self.enter is True:
                self.opening_screen_bool = False
                self.enter = False

        if self.opening_screen_bool is False:

            #displays most of the text in the game
            if self.text_boolean is True:
                self.textscreens.display_text(self.text_counter)

            #displays gameover screen
            if self.gameover is True:
                self.gameover_options.display_gameover()

            if self.text_boolean is False and self.gameover is False:
                #displays zombie stuff
                self.zm.attack_territory_fade()
                self.zm.display_zm()
                self.zm.display_health()

                #displays player stuff
                self.pl.display_pl()
                self.pl.display_health()

    def on_update(self, delta_time: float):

        if self.opening_screen_bool is False:

            #class-to-local conversions (not including cases variables are only needed upon certain conditions being met)
            self.gameover = self.pl.gameover_bool

            #dev mode
            if self.dev_mode is True:
                if self.pl.health != 15:
                    self.pl.health = 15
                    self.pl.hp_loc = self.pl.original_x
                    self.pl.hp_backwards_by = 0

            #text_logic
            if self.text_boolean is True:
                if self.enter is True and self.text_counter !=4:
                    self.text_boolean = False
                    self.enter = False
                elif self.enter is True:
                    exit()

            #restart/gameover
            if self.gameover is True:
                self.gameover_options.gameover_logic(self.screen_movements, self.enter)
                self.chooser_loc = self.gameover_options.chooser_loc
                self.restart = self.gameover_options.bool_restart
                if self.restart is True:
                    self.text_counter = 1
                    self.text_boolean = True
                    self.zm.restart()
                    self.pl.restart()
                    self.pl.gameover_bool = False
                    self.gameover_options.bool_restart = False

            #FPS logic
            self.FPS_counter += 1
            self.second_checker += delta_time
            if self.second_checker >= 1:
                self.FPS = self.FPS_counter
                self.FPS_counter = 0
                self.second_checker = 0

            if self.paused is False and self.FPS >= 30:
                if self.text_boolean is False and self.gameover is False:

                    #player logic
                    self.pl.time_start(delta_time)
                    self.pl.move(self.movements, delta_time)
                    for i in self.zm.boltlist:
                        if self.pl.x < i.center_x + self.damage_areas and self.pl.x > i.center_x - self.damage_areas and self.pl.y < i.center_y + self.damage_areas and self.pl.y > i.center_y - self.damage_areas and i.alpha == 250:
                            self.hit = True
                            self.pl.logic_health(self.hit, self.evolution)
                    if self.hit is True:
                        self.hit = False

                    #zombie logic
                    if self.evolution != self.zm.evolution:
                        self.evolution = self.zm.evolution
                        self.text_counter = self.evolution
                        self.text_boolean = True

                    self.zm.time_start(delta_time)
                    self.zm.move_zm(delta_time)
                    self.zm.attack_territory_display()
                    self.zm.logic_health(self.player_hit, self.pl.x, self.dev_mode)

                    if self.player_hit is True:
                        self.player_hit = False


if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.
    You can ignore this whole section. Keep it at the bottom
    of your code.
    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(WIDTH, HEIGHT, update_rate=1 / 70)
    my_view = Chapter4View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
