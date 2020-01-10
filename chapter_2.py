import arcade
import random

WIDTH = 800
HEIGHT = 600
MOVEMENT_SPEED = 3


class Room:
    pass


class Zombie_blood(arcade.Sprite):
    pass


class Antibiotic(arcade.Sprite):
    pass


class Vial(arcade.Sprite):
    pass


class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH - 1:
            self.right = WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        self.time = 30.00

        self.player_list = arcade.SpriteList()
        self.player = Player("player.png", 0.05)
        self.player.center_x = 100
        self.player.center_y = 100

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.zombie_blood = Zombie_blood("Blood.png", 0.02)
        self.zombie_blood.center_x = random.randrange(WIDTH)
        self.zombie_blood.center_y = random.randrange(HEIGHT)

    def on_draw(self):
        arcade.start_render()
        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        output = ("Time: {}: {}".format(minutes, seconds))

        self.player.draw()
        arcade.draw_text(output, WIDTH - 175, HEIGHT - 30, arcade.color.BLACK, 24)
        self.zombie_blood.draw()

    def update(self, delta_time):
        self.time -= delta_time
        self.player.update()
        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT)
    my_view = Chapter1View()
    window.show_view(my_view)
    arcade.run()


