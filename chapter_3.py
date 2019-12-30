import arcade
import random
import math
import os

WIDTH = 1000
HEIGHT = 700


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        self.player = arcade.Sprite(center_x=WIDTH/2, center_y=10)
        self.player.texture = arcade.make_soft_square_texture(50, arcade.color.ASH_GREY, outer_alpha=255)

        self.mouse = arcade.Sprite(center_x=100, center_y=100)
        self.mouse.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)

        self.enemy_texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)
        self.enemies = arcade.SpriteList()

        # create an enemy
        for _ in range(10):
            enemy = arcade.Sprite()
            enemy.center_x = random.randrange(0, WIDTH)
            enemy.center_y = random.randrange(HEIGHT+50, HEIGHT*2)
            enemy.change_y = -3
            enemy.texture = self.enemy_texture
            self.enemies.append(enemy)

        self.laser_texture = arcade.make_soft_square_texture(30, arcade.color.ORANGE, outer_alpha=255)
        self.lasers = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()

        self.player.draw()
        self.mouse.draw()
        self.enemies.draw()
        self.lasers.draw()

    def update(self, delta_time):
        self.lasers.update()
        self.enemies.update()

        for laser in self.lasers:
            laser_kill = arcade.check_for_collision_with_list(laser, self.enemies)
            if len(laser_kill) > 0:
                laser.kill()

        for enemy in self.enemies:
            enemy_kill = arcade.check_for_collision_with_list(enemy, self.lasers)
            if len(enemy_kill) > 0:
                enemy.kill()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse.center_x = x
        self.mouse.center_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        laser = arcade.Sprite()
        laser.center_x = self.player.center_x
        laser.center_y = self.player.center_y
        laser.texture = self.laser_texture
        laser.width = 5


        dest_x = x
        dest_y = y


        x_diff = dest_x - self.player.center_x
        y_diff = dest_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)


        self.laser = math.degrees(angle)


        laser.change_x = math.cos(angle) * 15
        laser.change_y = math.sin(angle) * 15

        self.lasers.append(laser)

def main():
    game = MyGame(WIDTH, HEIGHT, "My Game")
    arcade.run()


if __name__ == "__main__":
    main()
    
