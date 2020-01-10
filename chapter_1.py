import arcade
import math
import random
import settings
import os


class Zombie(arcade.Sprite):
    # def __init__(self, x: int, y: int, x_speed: int = 0, y_speed: int = 0):
    #     self.x = x
    #     self.y = y
    #     self.x_speed = x_speed
    #     self.y_speed = y_speed
    #     self.color = arcade.color.RED
    #
    #
    # def draw(self):
    #     arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

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


        # if self.x > settings.WIDTH or self.x < 0:
        #     self.x_speed = -self.x_speed
        #
        # if self.y > settings.HEIGHT or self.y < 0:
        #     self.y_speed = -self.y_speed

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

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("Images\player_right.png")
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        self.zombies = arcade.SpriteList()
        self.zombie_texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

        # self.gun_sound =
        # self.hit_sound =
        self.bullet_list = arcade.SpriteList()



        for i in range(3):
            # zombie = arcade.Sprite()
            zombie = Zombie("Images\zombie_right.png", 0.2)
            zombie.center_x = random.randrange(0, settings.WIDTH)
            zombie.center_y = random.randrange(settings.HEIGHT // 2, settings.HEIGHT)
            zombie.texture = self.zombie_texture
            self.zombies.append(zombie)

    def on_draw(self):
        arcade.start_render()
        # Draw in here...
        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        output = ("Time: {}: {}".format(minutes, seconds))

        self.player_list.draw()
        self.bullet_list.draw()
        self.zombies.draw()
        arcade.draw_text(output, settings.WIDTH - 175, settings.HEIGHT - 30,  arcade.color.BLACK, 24)

    def update(self, delta_time):
        self.time -= delta_time
        # self.zombies.update()
        self.player_sprite.update()
        self.bullet_list.update()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombies)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            if bullet.bottom > settings.WIDTH or bullet.top < 0 or bullet.right < 0 or bullet.left > settings.WIDTH:
                bullet.remove_from_sprite_lists()

        for zombie in self.zombies:
            zombie.follow_player(self.player_sprite)
        for s in self.zombies:
            player_in_contact = s.collides_with_list(self.player_list)
            if player_in_contact:
                print("HHHHHHHHHHHHHHHH")


    def on_key_press(self, key, modifiers):
        # self.director.next_view()
        if key == arcade.key.ESCAPE:
            pass
        if key == arcade.key.D:
            self.player_sprite.change_x = 5
        if key == arcade.key.A:
            self.player_sprite.change_x = -5
        if key == arcade.key.W:
            self.player_sprite.change_y = 5
        if key == arcade.key.S:
            self.player_sprite.change_y = -5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

    def mouse_press(self, x, y, button, modifiers):
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y


        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        self.bullet_list.append(bullet)




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
