import arcade
import random
import math
import settings


WIDTH = 800
HEIGHT = 600
MOVEMENT_SPEED = [-2, -3, -4, -5]


class Chapter3View(arcade.View):
    def __init__(self):
        super().__init__()
        global finish, bullet_speed, background, images
        finish = False

        # Sprite Images
        background_image = 'Chapter 3 Sprites/background.jpg'
        player_image = 'Chapter 3 Sprites/player.png'
        gun_image = 'Chapter 3 Sprites/gun.png'
        enemy_image = 'Chapter 3 Sprites/zombie.png'

        images = [background_image, player_image, gun_image, enemy_image]

        background = arcade.Sprite(images[0],
                                   center_x=WIDTH/2,
                                   center_y=HEIGHT/2,
                                   scale=1)

        arcade.set_background_color(arcade.color.BLACK)
        self.total_time = 31.0

        self.player = arcade.Sprite(images[1],
                                    center_x=WIDTH/2,
                                    center_y=0,
                                    scale=0.18)

        self.base = arcade.Sprite(center_x=WIDTH/2, center_y=-375, scale=1)
        base_color = arcade.color.BATTLESHIP_GREY
        self.base.texture = arcade.make_soft_square_texture(WIDTH,
                                                            base_color,
                                                            outer_alpha=255)

        self.gun = arcade.Sprite(images[2],
                                 center_x=WIDTH/2,
                                 center_y=-15,
                                 scale=0.13)

        self.mouse = arcade.Sprite(center_x=100, center_y=100)
        self.mouse.texture = arcade.make_soft_circle_texture(10,
                                                             arcade.color.RED,
                                                             outer_alpha=10)

        self.enemies = arcade.SpriteList()

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

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60

        # Texts
        pause_display = "Press ESC To Pause"
        timer = f"Time: {minutes:02d}:{seconds:02d}"
        timer_ends = "Mission Complete"
        goal = "Defend The Base"
        end_msg = "Click Enter to Advance"

        messages = [pause_display, timer, timer_ends, goal, end_msg]

        arcade.draw_text(messages[0],
                         600,
                         HEIGHT-40,
                         arcade.color.WHITE,
                         15)

        if seconds == 0:
            finish = True

        if finish is False:
            arcade.draw_text(messages[1],
                             10,
                             HEIGHT-40,
                             arcade.color.WHITE,
                             30)
        else:
            arcade.draw_text(messages[2],
                             10,
                             HEIGHT-40,
                             arcade.color.WHITE,
                             30)
        if seconds >= 28 and seconds <= 31:
            arcade.draw_text(messages[3],
                             WIDTH/2-160,
                             HEIGHT-100,
                             arcade.color.WHITE,
                             30)
        if finish is True:
            arcade.draw_text(messages[4],
                             WIDTH/2-190,
                             100,
                             arcade.color.WHITE,
                             30)

    def update(self, delta_time):
        global finish
        self.bullets.update()
        self.enemies.update()
        self.gun.update()
        self.spawn_enemy()
        self.collision()

        if finish is False:
            self.total_time -= delta_time

    def spawn_enemy(self):
        global finish, images
        if finish is False:
            if random.randrange(40) == 0:
                enemy = arcade.Sprite(images[3], scale=0.3)
                enemy.center_x = random.randrange(50, WIDTH-50)
                enemy.center_y = random.randrange(HEIGHT+50, HEIGHT*2)
                enemy.change_y = random.choice(MOVEMENT_SPEED)
                self.enemies.append(enemy)

    def collision(self):
        for enemy in self.enemies:
            bullets_in_contact = enemy.collides_with_list(self.bullets)
            if bullets_in_contact:
                enemy.kill()
                for bullet in bullets_in_contact:
                    bullet.kill()

        for enemy in self.enemies:
            base_in_contact = self.base.collides_with_list(self.enemies)
            if base_in_contact:
                enemy.kill()
                gameover = GameoverView(self)
                self.window.show_view(gameover)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mouse.center_x = x
        self.mouse.center_y = y

        # Allow gun to follow the direction of mouse
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

        # Bullet facing at an angle
        x_diff = x - bullet.center_x
        y_diff = y - bullet.center_y
        angle = math.atan2(y_diff, x_diff)

        bullet.angle = math.degrees(angle)
        bullet.change_x = math.cos(angle) * bullet_speed
        bullet.change_y = math.sin(angle) * bullet_speed
        self.bullets.append(bullet)

    def on_key_press(self, key, _modifiers):
        global finish
        if finish is True:
            if key == arcade.key.ENTER:
                self.director.next_view()
        if key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.draw_text("PAUSED", WIDTH/2, HEIGHT/2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press Esc. to return",
                         WIDTH/2,
                         HEIGHT/2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         WIDTH/2,
                         HEIGHT/2-30,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game = Chapter3View()
            self.window.show_view(game)


class GameoverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.draw_text("Game Over", WIDTH/2, HEIGHT/2+50,
                         arcade.color.RED, font_size=50, anchor_x="center")

        arcade.draw_text("Press Enter to Try Again",
                         WIDTH/2,
                         HEIGHT/2-30,
                         arcade.color.RED,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            game = Chapter3View()
            self.window.show_view(game)


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
