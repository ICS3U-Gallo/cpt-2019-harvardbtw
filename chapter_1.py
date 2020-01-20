import arcade
import math
import random
import settings


# Function to load the required images from the arcade resources folder
def load_texture_pair(filename):
    player_scaling = settings.SPRITE_SCALING_PLAYER
    return [
        arcade.load_texture(filename, scale=player_scaling),
        arcade.load_texture(filename, scale=player_scaling, mirrored=True)
    ]


class StartScreen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        title = "Dodge the Zombies"
        text = "Press Enter to read the instructions"
        x1 = settings.WIDTH/2
        y1 = settings.HEIGHT/2

        arcade.draw_text(title, x1, y1, arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(text, settings.WIDTH/2, settings.HEIGHT/2-75, arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        instructions_view = InstructionView()
        # Passes the director to the next view
        instructions_view.director = self.director
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        font_size = 16
        text_colour = arcade.color.BLACK

        # Instructions for the game
        text_1 = "A Zombie Apocalypse has just broke out and you must survive from the incoming zombies"
        text_2 = "until rescue arrives."
        text_3 = "You have 30 seconds to dodge 3 waves of zombies that spawn at the top of the screen."
        text_4 = "The 1st wave are regular zombies that walk around aimlessly."
        text_5 = "The 2nd wave of zombies are slow, but able to follow you around."
        text_6 = "The 3rd and final wave of zombies are fast but can't follow you like the previous wave."
        text_7 = "While you are being attacked by zombies, collect as many coins as you can to increase score"
        text_8 = "W = Player moves up"
        text_9 = "S = Player moves down"
        text_10 = "A = Player moves left"
        text_11 = "D = Player moves right"
        text_12 = "Use WASD to move"

        arcade.draw_text(text_1, 750, settings.HEIGHT - 50, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_2, 180, settings.HEIGHT - 100, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_3, 720, settings.HEIGHT - 150, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_4, 520, settings.HEIGHT - 200, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_5, 550, settings.HEIGHT - 250, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_6, 720, settings.HEIGHT - 300, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_7, 770, settings.HEIGHT - 350, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_12, 200, settings.HEIGHT - 380, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_8, 210, settings.HEIGHT - 410, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_9, 225, settings.HEIGHT - 440, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_10, 208, settings.HEIGHT - 470, text_colour, font_size, anchor_x="right")
        arcade.draw_text(text_11, 210, settings.HEIGHT - 500, text_colour, font_size, anchor_x="right")
        arcade.draw_text("Press Enter to play", settings.WIDTH/2, 50, arcade.color.GRAY, font_size=30, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            chapter1_view = Chapter1View()
            # Passes director to the Chapter 1 View (Game View)
            chapter1_view.director = self.director
            self.window.show_view(chapter1_view)


class Coin(arcade.Sprite):
    def draw(self):
        # sets the coin position to a random location on the screen
        self.center_y = random.randrange(settings.HEIGHT + 20, settings.HEIGHT + 100)
        self.center_x = random.randrange(settings.WIDTH)


class Level1Zombie(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Sets default direction to right
        self.zombie_face_direction = settings.RIGHT_FACING

        # Used to flip between image pairs
        self.current_texture = 0

        # Adjusts the image hitbox to remove all whitespaces found in image
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # Sets the path in which the image is found in
        main_path = ":resources:images/animated_characters/zombie/zombie"

        # Loads textures for idle image
        self.idle_texture_pair = load_texture_pair("{}_idle.png".format(main_path))

        # Loads textures for walking image
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair("{}_walk{}.png".format(main_path, i))
            self.walk_textures.append(texture)

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Determines which direction to flip image in
        if self.change_x < 0 and self.zombie_face_direction == settings.RIGHT_FACING:
            self.zombie_face_direction = settings.LEFT_FACING
        elif self.change_x > 0 and self.zombie_face_direction == settings.LEFT_FACING:
            self.zombie_face_direction = settings.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.zombie_face_direction]
            return

        # Walking animation
        self.current_texture += 1
        if self.current_texture > 7 * settings.UPDATES_PER_FRAME:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture // settings.UPDATES_PER_FRAME][self.zombie_face_direction]

        # Makes the image go in the opposite direction if it reaches the screen border
        if self.center_x > settings.WIDTH or self.center_x < 0:
            self.change_x = -self.change_x

        if self.center_y > settings.HEIGHT or self.center_y < 0:
            self.change_y = -self.change_y


class Level2Zombie(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.zombie_face_direction = settings.RIGHT_FACING
        self.current_texture = 0

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = ":resources:images/animated_characters/zombie/zombie"

        self.idle_texture_pair = load_texture_pair("{}_idle.png".format(main_path))

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair("{}_walk{}.png".format(main_path, i))
            self.walk_textures.append(texture)

    def follow_player(self, player_sprite):
        # This function will make the level 2 zombies follow the player sprite
        self.center_x += self.change_x
        self.center_y += self.change_y

        start_x = self.center_x
        start_y = self.center_y

        # Gets the destination for the zombies as the player's position
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Calculates the distance and angle between the zombie and the player
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle between the player and zombie,
        # this calculates the zombie's change_x and change_y
        self.change_x = math.cos(angle) * settings.LEVEL2_ZOMBIE_SPEED
        self.change_y = math.sin(angle) * settings.LEVEL2_ZOMBIE_SPEED

        # Determines direction to face in
        if self.change_x < 0 and self.zombie_face_direction == settings.RIGHT_FACING:
            self.zombie_face_direction = settings.LEFT_FACING
        elif self.change_x > 0 and self.zombie_face_direction == settings.LEFT_FACING:
            self.zombie_face_direction = settings.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.zombie_face_direction]
            return

        # Walking animation
        self.current_texture += 1
        if self.current_texture > 7 * settings.UPDATES_PER_FRAME:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture // settings.UPDATES_PER_FRAME][self.zombie_face_direction]

        if self.center_x > settings.WIDTH or self.center_x < 0:
            self.change_x = -self.change_x

        if self.center_y > settings.HEIGHT or self.center_y < 0:
            self.change_y = -self.change_y


class Level3Zombie(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.zombie_face_direction = settings.RIGHT_FACING
        self.current_texture = 0

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = ":resources:images/animated_characters/zombie/zombie"

        self.idle_texture_pair = load_texture_pair("{}_idle.png".format(main_path))

        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair("{}_walk{}.png".format(main_path, i))
            self.walk_textures.append(texture)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Determines direction to face
        if self.change_x < 0 and self.zombie_face_direction == settings.RIGHT_FACING:
            self.zombie_face_direction = settings.LEFT_FACING
        elif self.change_x > 0 and self.zombie_face_direction == settings.LEFT_FACING:
            self.zombie_face_direction = settings.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.zombie_face_direction]
            return

        # Walking animation
        self.current_texture += 1
        if self.current_texture > 7 * settings.UPDATES_PER_FRAME:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture // settings.UPDATES_PER_FRAME][self.zombie_face_direction]

        if self.center_x > settings.WIDTH or self.center_x < 0:
            self.change_x = -self.change_x

        if self.center_y > settings.HEIGHT or self.center_y < 0:
            self.change_y = -self.change_y


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.player_face_direction = settings.RIGHT_FACING
        self.current_texture = 0

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = ":resources:images/animated_characters/male_person/malePerson"

        self.idle_texture_pair = load_texture_pair("{}_idle.png".format(main_path))

        self.walk_textures = []

        for i in range(8):
            texture = load_texture_pair("{}_walk{}.png".format(main_path, i))
            self.walk_textures.append(texture)

    def update(self, delta_time: float = 1/60):
        # Creates screen border for player
        # Can only move while within the given screen size
        if self.left < 0:
            self.left = 0
        elif self.right > settings.WIDTH - 1:
            self.right = settings.WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > settings.HEIGHT - 1:
            self.top = settings.HEIGHT - 1

        # Determines direction to face in
        if self.change_x < 0 and self.player_face_direction == settings.RIGHT_FACING:
            self.player_face_direction = settings.LEFT_FACING

        elif self.change_x > 0 and self.player_face_direction == settings.LEFT_FACING:
            self.player_face_direction = settings.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.player_face_direction == 0:
            self.texture = self.idle_texture_pair[self.player_face_direction]
            return

        # Walking animation
        self.current_texture += 1
        if self.current_texture > 7 * settings.UPDATES_PER_FRAME:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture // settings.UPDATES_PER_FRAME][self.player_face_direction]

        self.center_x += self.change_x
        self.center_y += self.change_y


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GREEN)

        # Creates game timer and sets it to 30 seconds
        self.time = 5

        # Creates score counter
        self.score = 0

        # Sets up coin
        self.coin_sprite_list = arcade.SpriteList()

        # Sets up player
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = settings.WIDTH / 2
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        # Sets up level 1 zombies
        self.level1_zombies = arcade.SpriteList()

        # Sets up level 2 zombies
        self.level2_zombies = arcade.SpriteList()

        # Sets up level 3 zombies
        self.level3_zombies = arcade.SpriteList()

        # Creates the level 1 zombies
        for level1 in range(settings.LEVEL1_ZOMBIE_COUNT):
            zombie = Level1Zombie()
            # Positions the zombies
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = (settings.HEIGHT - 50)
            # Gives zombie speed
            zombie.change_x = random.choice(settings.LEVEL1_ZOMBIE_SPEED)
            zombie.change_y = random.choice(settings.LEVEL1_ZOMBIE_SPEED)

            self.level1_zombies.append(zombie)

        # Creates the level 2 zombies
        for level2 in range(settings.LEVEL2_ZOMBIE_COUNT):
            zombie = Level2Zombie()
            # Positions zombies
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = (settings.HEIGHT - 50)
            self.level2_zombies.append(zombie)

        # Creates the level 3 zombies
        for level3 in range(settings.LEVEL3_ZOMBIE_COUNT):
            zombie = Level3Zombie()
            # Positions zombies
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = random.randrange(settings.HEIGHT - 50)
            # Gives zombie speed
            zombie.change_x = random.choice(settings.LEVEL3_ZOMBIE_SPEED)
            zombie.change_y = random.choice(settings.LEVEL3_ZOMBIE_SPEED)

            self.level3_zombies.append(zombie)

        # Creates the coins
        for coin in range(settings.COIN_COUNT):
            coin = Coin("Chapter1_Images\coin.png", settings.SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(settings.WIDTH)
            coin.center_y = random.randrange(settings.HEIGHT)

            self.coin_sprite_list.append(coin)

    def on_draw(self):
        arcade.start_render()
        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        time_output = ("Time: {}: {}".format(minutes, seconds))
        score_output = ("Score: {}".format(self.score))

        # Draws all sprites
        self.coin_sprite_list.draw()
        self.player_list.draw()
        self.level1_zombies.draw()
        if self.time <= 20:
            self.level2_zombies.draw()
        if self.time <= 10:
            self.level3_zombies.draw()

        # Draws time remaining and total score
        arcade.draw_text(time_output, settings.WIDTH - 175, settings.HEIGHT - 30,  arcade.color.BLACK, 24)
        arcade.draw_text(score_output, settings.WIDTH - 790, settings.HEIGHT - 30, arcade.color.BLACK, 24)

    def update(self, delta_time):
        # Decreases timer by 1 until it reaches 0
        if self.time > 0:
            self.time -= delta_time

        # Once the time hits 0, player wins and is sent to game_win_view
        if self.time <= 0:
            game_win_view = GameWinView()
            # Passes director to the game_win_view
            game_win_view.director = self.director
            game_win_view.score = self.score
            self.window.show_view(game_win_view)

        # Updates the sprite lists
        self.player_sprite.update()
        self.coin_sprite_list.update()
        self.level1_zombies.update()
        self.level3_zombies.update()

        # Checks if player collides with a coin
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)

        # If player collides with coin, increase score by 1
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Checks for player collision with level 1 zombies
        for level1_zombie in self.level1_zombies:
            player_in_contact = level1_zombie.collides_with_list(self.player_list)
            if player_in_contact:
                game_over_view = GameOverView()
                game_over_view.director = self.director
                game_over_view.score = self.score
                self.window.show_view(game_over_view)

        # Checks for player collision with level 2 zombies
        if self.time <= 20:
            for level2_zombie in self.level2_zombies:
                level2_zombie.follow_player(self.player_sprite)

            for zombie in self.level2_zombies:
                player_in_contact = zombie.collides_with_list(self.player_list)
                if player_in_contact:
                    game_over_view = GameOverView()
                    game_over_view.director = self.director
                    game_over_view.score = self.score
                    self.window.show_view(game_over_view)

        # Checks for player collision with level 3 zombies
        if self.time <= 10:
            for level3_zombie in self.level3_zombies:
                player_in_contact = level3_zombie.collides_with_list(self.player_list)
                if player_in_contact:
                    game_over_view = GameOverView()
                    game_over_view.director = self.director
                    game_over_view.score = self.score
                    self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        # Creates controls for player movement
        if key == arcade.key.D:
            self.player_sprite.change_x = settings.PLAYER_SPEED
        if key == arcade.key.A:
            self.player_sprite.change_x = -settings.PLAYER_SPEED
        if key == arcade.key.W:
            self.player_sprite.change_y = settings.PLAYER_SPEED
        if key == arcade.key.S:
            self.player_sprite.change_y = -settings.PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        # Makes player stop when releasing keys
        if key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0


class GameWinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        text_1 = "Congratulations you won! You survived the"
        text_2 = "zombies long enough for rescue to arrive!"
        text_3 = "Your score was {}".format(self.score)
        text_4 = "Press space to advance to the next chapter"

        arcade.draw_text(text_1, 80, 400, arcade.color.BLACK, 28)
        arcade.draw_text(text_2, 80, 350, arcade.color.BLACK, 28)
        arcade.draw_text(text_3, settings.WIDTH/2, 80, arcade.color.BLACK, 24, anchor_x="center")
        arcade.draw_text(text_4, settings.WIDTH/2, 280, arcade.color.BLACK, 24, anchor_x="center")

    def on_key_press(self, key, modifiers):
        # If player presses space, advance to the next chapter
        if key == arcade.key.SPACE:
            self.director.next_view()


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        text_1 = "Game Over! You were eaten by zombies."
        text_2 = "Your score was {}".format(self.score)
        text_3 = "Click to restart"

        arcade.draw_text(text_1, 50, 400, arcade.color.BLACK, 34)
        arcade.draw_text(text_2, settings.WIDTH/2, 300, arcade.color.BLACK, 34, anchor_x="center")
        arcade.draw_text(text_3, 310, 200, arcade.color.BLACK, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # If player clicks the screen, restart the game
        game_view = Chapter1View()
        game_view.director = self.director
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
    my_view = StartScreen()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
