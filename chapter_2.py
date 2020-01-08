
import arcade

WIDTH = 800
HEIGHT = 600


class Player:
    def __init__(self, x, y, x_speed, y_speed, radius, color):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = radius
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def update(self):
        self.y += self.x_speed
        self.x += self.y_speed


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.ball = Player(50, 50, 0, 0, 15, arcade.color.AUBURN)

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()

    def update(self, delta_time):
        self.ball.update()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.ball.change_x = -5
        elif key == arcade.key.D:
            self.ball.change_x = 5
        elif key == arcade.key.W:
            self.ball.change_y = 5
        elif key == arcade.key.S:
            self.ball.change_y = -5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.ball.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.ball.change_y = 0

    def on_mouse_press(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    MyGame(WIDTH, HEIGHT, "OK")
    arcade.run()
