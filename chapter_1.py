import arcade
import math
import random
import settings
import os


class Coin(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(settings.HEIGHT + 20, settings.HEIGHT + 100)
        self.center_x = random.randrange(settings.WIDTH)

    def update(self):
        # self.center_y -= 1
        if self.top < 0:
            self.reset_pos()


class Level1_Zombie(arcade.Sprite):
    def update(self):
        # self.change_x = random.randrange(-2, 2)
        # self.change_y = random.randrange(-2, 2)
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > settings.WIDTH or self.center_x < 0:
            self.change_x = -self.change_x

        if self.center_y > settings.HEIGHT or self.center_y < 0:
            self.change_y = -self.change_y


class Level2_Zombie(arcade.Sprite):
    def follow_player(self, player_sprite):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # if random.randrange(100) == 0:
        start_x = self.center_x
        start_y = self.center_y

        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = math.cos(angle) * settings.ZOMBIE_SPEED
        self.change_y = math.sin(angle) * settings.ZOMBIE_SPEED


class Level3_Zombie(arcade.Sprite):
    pass


class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > settings.WIDTH - 1:
            self.right = settings.WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > settings.HEIGHT - 1:
            self.top = settings.HEIGHT - 1


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GREEN)

        self.time = 30.00
        self.score = 0

        self.coin_sprite_list = arcade.SpriteList()

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("Images\player_right.png")
        self.player_sprite.center_x = settings.WIDTH / 2
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        self.level1_zombies = arcade.SpriteList()
        # self.zombie_texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

        self.level2_zombies = arcade.SpriteList()
        self.level3_zombies = arcade.SpriteList()

        # self.gun_sound =
        # self.hit_sound =

        for i in range(8):
            # zombie = arcade.Sprite()
            zombie = Level2_Zombie("Images\zombie_right.png", settings.SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = random.randrange(settings.HEIGHT // 2, settings.HEIGHT)
            # zombie.texture = self.zombie_texture
            self.level2_zombies.append(zombie)

        for j in range(2):
            zombie = Level1_Zombie("Images\zombie_left.png", settings.SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = random.randrange(settings.HEIGHT // 2, settings.HEIGHT)
            zombie.change_x = random.randrange(-2, 2)
            zombie.change_y = random.randrange(-2, 2)

            self.level1_zombies.append(zombie)

        for k in range(settings.COIN_COUNT):
            coin = Coin("Images\coin.png", settings.SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(settings.WIDTH)
            coin.center_y = random.randrange(settings.HEIGHT)

            self.coin_sprite_list.append(coin)

    def on_draw(self):
        arcade.start_render()
        # Draw in here...
        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        time_output = ("Time: {}: {}".format(minutes, seconds))
        score_output = ("Score: {}".format(self.score))

        self.coin_sprite_list.draw()
        self.player_list.draw()
        self.level1_zombies.draw()
        self.level2_zombies.draw()

        arcade.draw_text(time_output, settings.WIDTH - 175, settings.HEIGHT - 30,  arcade.color.BLACK, 24)
        arcade.draw_text(score_output, settings.WIDTH - 790, settings.HEIGHT - 30, arcade.color.BLACK, 24)

    def update(self, delta_time):
        self.time -= delta_time
        # self.zombies.update()
        self.player_sprite.update()
        self.coin_sprite_list.update()
        # self.level1_zombies.update()
        self.level1_zombies.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)

        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        for i in self.level1_zombies:
            player_in_contact = i.collides_with_list(self.player_list)
            if player_in_contact:
                print("oof")

        for zombie in self.level2_zombies:
            zombie.follow_player(self.player_sprite)

        for s in self.level2_zombies:
            player_in_contact = s.collides_with_list(self.player_list)
            if player_in_contact:
                print("HHHHHHHHHHHHHHHH")

    def on_key_press(self, key, modifiers):
        # self.director.next_view()
        if key == arcade.key.ESCAPE:
            pass
        if key == arcade.key.D:
            self.player_sprite.change_x = settings.PLAYER_SPEED_POSITIVE
        if key == arcade.key.A:
            self.player_sprite.change_x = settings.PLAYER_SPEED_NEGATIVE
        if key == arcade.key.W:
            self.player_sprite.change_y = settings.PLAYER_SPEED_POSITIVE
        if key == arcade.key.S:
            self.player_sprite.change_y = settings.PLAYER_SPEED_NEGATIVE

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

    def mouse_press(self, x, y, button, modifiers):
        pass


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
    my_view = Chapter1View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
