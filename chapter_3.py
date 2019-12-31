import arcade
import random
import math
import os

WIDTH = 1000
HEIGHT = 700

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        global finish, bullet_speed

        arcade.set_background_color(arcade.color.BLACK)
        self.set_mouse_visible(False)
        self.total_time = 30.0
        finish = False

        self.player = arcade.Sprite(center_x=WIDTH/2, center_y=10)
        self.player.texture = arcade.make_soft_square_texture(50, arcade.color.ASH_GREY, outer_alpha=255)

        self.base = arcade.Sprite(center_x=WIDTH/2, center_y=-475)
        self.base.texture = arcade.make_soft_square_texture(WIDTH, arcade.color.BATTLESHIP_GREY, outer_alpha=255)

        self.mouse = arcade.Sprite(center_x=100, center_y=100)
        self.mouse.texture = arcade.make_soft_circle_texture(10, arcade.color.RED, outer_alpha=10)

        self.enemy_texture = arcade.make_soft_circle_texture(50, arcade.color.GREEN, outer_alpha=255)
        self.enemies = arcade.SpriteList()

        # create an enemy
        for _ in range(10):
            enemy = arcade.Sprite()
            enemy.center_x = random.randrange(0, WIDTH)
            enemy.center_y = random.randrange(HEIGHT+50, HEIGHT*2)
            enemy.change_y = -3
            enemy.texture = self.enemy_texture
            self.enemies.append(enemy)

        self.bullet_texture = arcade.make_soft_square_texture(10, arcade.color.ORANGE, outer_alpha=255)
        self.bullets = arcade.SpriteList()
        bullet_speed = 15

    def on_draw(self):
        global finish
        arcade.start_render()

        self.enemies.draw()
        self.base.draw()
        self.player.draw()
        self.mouse.draw()
        self.bullets.draw()

#Timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"

        if seconds == 0:
            finish = True
            arcade.draw_text("Mission Complete", 10, HEIGHT-40, arcade.color.WHITE, 30)

        if finish == False:
            arcade.draw_text(output, 10, HEIGHT-40, arcade.color.WHITE, 30)

    def update(self, delta_time):
        global finish
        self.bullets.update()
        self.enemies.update()

# Update Timer
        self.total_time -= delta_time


# Update Bullet
        for bullet in self.bullets:
            bullet_kill = arcade.check_for_collision_with_list(bullet, self.enemies)
            if len(bullet_kill) > 0:
                bullet.kill()

        for enemy in self.enemies:
            enemy_kill = arcade.check_for_collision_with_list(enemy, self.bullets)
            if len(enemy_kill) > 0:
                enemy.kill()


    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse.center_x = x
        self.mouse.center_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        global bullet_speed
        bullet = arcade.Sprite()
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y
        bullet.texture = self.bullet_texture
        bullet.width = 20

        dest_x = x
        dest_y = y


        x_diff = dest_x - self.player.center_x
        y_diff = dest_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)


        bullet.angle = math.degrees(angle)


        bullet.change_x = math.cos(angle) * bullet_speed
        bullet.change_y = math.sin(angle) * bullet_speed

        self.bullets.append(bullet)

def main():
    game = MyGame(WIDTH, HEIGHT, "My Game")
    arcade.run()


if __name__ == "__main__":
    main()
