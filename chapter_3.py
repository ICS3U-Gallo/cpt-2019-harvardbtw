import arcade
import random
import math
import os
import settings


WIDTH = 800
HEIGHT = 600


class Chapter3View(arcade.View):
    def on_show(self):
        global finish, bullet_speed, background
        background = arcade.Sprite('Chapter 3 Sprites/background.jpg', center_x=WIDTH/2, center_y=HEIGHT/2, scale=1)

        arcade.set_background_color(arcade.color.BLACK)
        self.total_time = 31.0
        finish = False

# Player
        self.player = arcade.Sprite(center_x=WIDTH/2, center_y=0)
        self.player.texture = arcade.make_soft_circle_texture(100, arcade.color.ASH_GREY, outer_alpha=255)
# Base
        self.base = arcade.Sprite(center_x=WIDTH/2, center_y=-375)
        self.base.texture = arcade.make_soft_square_texture(WIDTH, arcade.color.BATTLESHIP_GREY, outer_alpha=255)
# Gun
        self.gun = arcade.Sprite('Chapter 3 Sprites/gun.png', center_x=WIDTH/2, center_y=-15, scale=0.13)
# Red Dot
        self.mouse = arcade.Sprite(center_x=100, center_y=100)
        self.mouse.texture = arcade.make_soft_circle_texture(10, arcade.color.RED, outer_alpha=10)
# Enemy
        self.enemy_texture = arcade.make_soft_circle_texture(50, arcade.color.GREEN, outer_alpha=255)
        self.enemies = arcade.SpriteList()        
            
# Bullet
        self.bullets = arcade.SpriteList()
        bullet_speed = 50

    def on_draw(self):
        global finish
        arcade.start_render()

        background.draw()
        self.enemies.draw()
        self.bullets.draw()
        self.base.draw()
        self.gun.draw()
        self.player.draw()
        self.mouse.draw()

#Timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        goal = "Defend The Base"

        if seconds == 0:
            finish = True

        if finish is False:
            arcade.draw_text(output, 10, HEIGHT-40, arcade.color.WHITE, 30)
        if seconds >= 28:
            arcade.draw_text(goal, WIDTH/2-150, HEIGHT-80, arcade.color.WHITE, 30)

    def update(self, delta_time):
        global finish
        self.bullets.update()
        self.enemies.update()
        self.gun.update()

# Update Timer
        if finish is False:
            self.total_time -= delta_time

# Spawn Enemies
        if finish is False:
            if random.randrange(30) == 0:
                enemy = arcade.Sprite()
                enemy.center_x = random.randrange(50, WIDTH-50)
                enemy.center_y = random.randrange(HEIGHT+50, HEIGHT*2)
                enemy.change_y = -3
                enemy.texture = self.enemy_texture
                self.enemies.append(enemy)
                

# Update Bullet
        for enemy in self.enemies:
            bullets_in_contact = enemy.collides_with_list(self.bullets)
            if bullets_in_contact:  
                enemy.kill()
                for bullet in bullets_in_contact:
                    bullet.kill()

        for enemy in self.enemies:
            bullets_in_contact = self.base.collides_with_list(self.enemies)
            if bullets_in_contact:
                enemy.kill()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse.center_x = x
        self.mouse.center_y = y

        self.gun.height = 300
        x_diff = x - self.gun.center_x
        y_diff = y - self.gun.center_y
        angle = math.atan2(y_diff, x_diff)
        self.gun.angle = math.degrees(angle)

    def on_mouse_press(self, x, y, button, key_modifiers):
        global bullet_speed
        bullet = arcade.Sprite('Chapter 3 Sprites/bullet.png', scale=0.02)
        bullet.center_x = WIDTH/2
        bullet.center_y = -10

        x_diff = x - bullet.center_x 
        y_diff = y - bullet.center_y
        angle = math.atan2(y_diff, x_diff)

        bullet.angle = math.degrees(angle)
        bullet.change_x = math.cos(angle) * bullet_speed
        bullet.change_y = math.sin(angle) * bullet_speed
        self.bullets.append(bullet)


if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.
    You can ignore this whole section. Keep it at the bottom
    of your code.
    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Chapter3View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
