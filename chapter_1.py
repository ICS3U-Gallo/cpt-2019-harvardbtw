import math
import random

import arcade


WIDTH = 640
HEIGHT = 480


class Sprite:
    def __init__(self, x: int, y: int, x_speed: int = 0, y_speed: int = 0):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = 25
        self.color = arcade.color.BLUE

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.x > WIDTH or self.x < 0:
            self.x_speed = -self.x_speed

        if self.y > HEIGHT or self.y < 0:
            self.y_speed = -self.y_speed


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.sprite1 = arcade.Sprite(center_x=100, center_y=200)
        self.sprite1.change_x = 0
        self.sprite1.change_y = 0
        self.sprite1.texture = arcade.make_soft_square_texture(50,
                                                               arcade.color.BLACK,
                                                               outer_alpha=255)


        self.sprites = []

        for _ in range(5):
            x = random.randrange(WIDTH)
            y = random.randrange(HEIGHT)
            dx = random.randrange(-5, 5)
            dy = random.randrange(-5, 5)

            s = Sprite(x, y, dx, dy)
            self.sprites.append(s)

    def update(self, delta_time):
        self.sprite1.update()
        self.sprite1.center_x += self.sprite1.change_x
        self.sprite1.center_y += self.sprite1.change_y
        for s in self.sprites:
            s.update()

    def on_draw(self):
        arcade.start_render()
        # Draw in here...
        self.sprite1.draw()
        for s in self.sprites:
            s.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.sprite1.change_x = 2.5

        if key == arcade.key.A:
            self.sprite1.change_x = -2.5

        if key == arcade.key.W:
            self.sprite1.change_y = 2.5

        if key == arcade.key.S:
            self.sprite1.change_y = -2.5

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass
        # for s in self.sprites:
        #     a = s.x - x
        #     b = s.y - y
        #     dist = math.sqrt(a**2 + b**2)
        #
        #     if dist < s.radius:
        #         s.radius += 5
        #         if s.radius > 50:
        #             self.sprites.remove(s)


if __name__ == '__main__':
    window = MyGame(WIDTH, HEIGHT, "My Arcade Game")
    arcade.run()
