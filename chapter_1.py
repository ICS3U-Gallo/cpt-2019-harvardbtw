import arcade
import math
import random
import settings


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, scale=settings.SPRITE_SCALING_PLAYER),
        arcade.load_texture(filename, scale=settings.SPRITE_SCALING_PLAYER, mirrored=True)
    ]

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Dodge the Zombies!!", settings.WIDTH/2, settings.HEIGHT/2, arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click anywhere to start", settings.WIDTH/2, settings.HEIGHT/2-75, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", settings.WIDTH/2, settings.HEIGHT/2, arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", settings.WIDTH/2, settings.HEIGHT/2-75, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        chapter1_view = Chapter1View()
        self.window.show_view(chapter1_view)


class Coin(arcade.Sprite):
    def draw(self):
        self.center_y = random.randrange(settings.HEIGHT + 20, settings.HEIGHT + 100)
        self.center_x = random.randrange(settings.WIDTH)


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

        self.change_x = math.cos(angle) * settings.LEVEL1_ZOMBIE_SPEED
        self.change_y = math.sin(angle) * settings.LEVEL1_ZOMBIE_SPEED


class Level3_Zombie(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x > settings.WIDTH or self.center_x < 0:
            self.change_x = -self.change_x

        if self.center_y > settings.HEIGHT or self.center_y < 0:
            self.change_y = -self.change_y


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = settings.RIGHT_FACING
        self.cur_texture = 0

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

        self.idle_texture_pair = load_texture_pair("{}_idle.png".format(main_path))

        self.walk_textures = []

        for i in range(8):
            texture = load_texture_pair("{}_walk{}.png".format(main_path, i))
            self.walk_textures.append(texture)

    def update(self, delta_time: float = 1/60):

        if self.left < 0:
            self.left = 0
        elif self.right > settings.WIDTH - 1:
            self.right = settings.WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > settings.HEIGHT - 1:
            self.top = settings.HEIGHT - 1

        if self.change_x < 0 and self.character_face_direction == settings.RIGHT_FACING:
            self.character_face_direction = settings.LEFT_FACING

        elif self.change_x > 0 and self.character_face_direction == settings.LEFT_FACING:
            self.character_face_direction = settings.RIGHT_FACING

        if self.change_x == 0 and self.character_face_direction == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 7 * settings.UPDATES_PER_FRAME:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture // settings.UPDATES_PER_FRAME][self.character_face_direction]
        self.center_x += self.change_x
        self.center_y += self.change_y


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GREEN)

        self.time = 5
        self.score = 0

        self.coin_sprite_list = arcade.SpriteList()

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player() # "Chapter1_Images\player_right.png"
        self.player_sprite.center_x = settings.WIDTH / 2
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        self.level1_zombies = arcade.SpriteList()
        # self.zombie_texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

        self.level2_zombies = arcade.SpriteList()
        self.level3_zombies = arcade.SpriteList()

        level1_zombie_speed = [-2, 2]

        level3_zombie_speed = [-6, 6]

        # self.gun_sound =
        # self.hit_sound =

        for level1 in range(4):
            zombie = Level1_Zombie("Chapter1_Images\zombie_left.png", settings.SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = (settings.HEIGHT - 50)
            zombie.change_x = random.choice(level1_zombie_speed)
            zombie.change_y = random.choice(level1_zombie_speed)

            self.level1_zombies.append(zombie)

        for level2 in range(0):
            # zombie = arcade.Sprite()
            zombie = Level2_Zombie("Chapter1_Images\zombie_right.png", settings.SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = (settings.HEIGHT - 50)
            # zombie.texture = self.zombie_texture
            self.level2_zombies.append(zombie)

        for level3 in range(0):
            zombie = Level3_Zombie("Chapter1_Images\zombie_right.png", settings.SPRITE_SCALING_ZOMBIE)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = random.randrange(settings.HEIGHT - 50)
            zombie.change_x = random.choice(level3_zombie_speed)
            zombie.change_y = random.choice(level3_zombie_speed)

            self.level3_zombies.append(zombie)

        for coin in range(settings.COIN_COUNT):
            coin = Coin("Chapter1_Images\coin.png", settings.SPRITE_SCALING_COIN)
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
        if self.time <= 20:
            self.level2_zombies.draw()
        if self.time <= 10:
            self.level3_zombies.draw()

        arcade.draw_text(time_output, settings.WIDTH - 175, settings.HEIGHT - 30,  arcade.color.BLACK, 24)
        arcade.draw_text(score_output, settings.WIDTH - 790, settings.HEIGHT - 30, arcade.color.BLACK, 24)

    def update(self, delta_time):
        if self.time >= 0:
            self.time -= delta_time

        elif self.time <= 0:
            game_win_view = GameWinView()
            self.window.show_view(game_win_view)
        # self.zombies.update()
        self.player_sprite.update()
        self.coin_sprite_list.update()
        # self.level1_zombies.update()
        self.level1_zombies.update()
        self.level3_zombies.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)

        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        for level1_zombie in self.level1_zombies:
            player_in_contact = level1_zombie.collides_with_list(self.player_list)
            if player_in_contact:
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)


        if self.time <= 20:
            for level2_zombie in self.level2_zombies:
                level2_zombie.follow_player(self.player_sprite)

            for zombie in self.level2_zombies:
                player_in_contact = zombie.collides_with_list(self.player_list)
                if player_in_contact:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)

        if self.time <= 10:
            for level3_zombie in self.level3_zombies:
                player_in_contact = level3_zombie.collides_with_list(self.player_list)
                if player_in_contact:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)


    def on_key_press(self, key, modifiers):
        # self.director.next_view()
        if key == arcade.key.ESCAPE:
            pass
        if key == arcade.key.D:
            self.player_sprite.change_x = settings.PLAYER_SPEED
        if key == arcade.key.A:
            self.player_sprite.change_x = -settings.PLAYER_SPEED
        if key == arcade.key.W:
            self.player_sprite.change_y = settings.PLAYER_SPEED
        if key == arcade.key.S:
            self.player_sprite.change_y = -settings.PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

    def mouse_press(self, x, y, button, modifiers):
        pass


class GameWinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Congratulations, you won! You survived the", 80, 400, arcade.color.BLACK, 28)
        arcade.draw_text("zombies long enough for rescue to arrive!", 80, 350, arcade.color.BLACK, 28)

        arcade.draw_text("Click space to advance to the next chapter", 80, 300, arcade.color.BLACK, 24)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over! You were eaten by zombies. :()", 120, 400, arcade.color.BLACK, 40)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.BLACK, 24)
        # score_output = "Total Score: {}".format(self.score)
        # arcade.draw_text(score_output, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Chapter1View()
        self.window.show_view(game_view)


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
    my_view = MenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
