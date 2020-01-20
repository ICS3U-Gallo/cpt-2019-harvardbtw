import arcade
import random
import math

WIDTH = 800
HEIGHT = 600
MOVEMENT_SPEED = 4
GRAVITY = 0.7
PLAYER_JUMP_SPEED = 12


class Start(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to Part 2! ", WIDTH / 2, HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        story_view = StoryView()
        story_view.director = self.director
        self.window.show_view(story_view)


class StoryView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Story", WIDTH / 2, 530,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, 470,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("You have been infected and have 30 seconds to live!",
                         50, HEIGHT / 2 + 100, arcade.color.WHITE, font_size=20
                         )
        arcade.draw_text("Collect all the ingredients to cure yourself!", 50,
                         HEIGHT / 2, arcade.color.WHITE, font_size=20)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        instructions_view.director = self.director
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.item_list = arcade.SpriteList()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        zombie_blood = arcade.Sprite("Chapter 2 Sprites/Blood.png", 0.2)
        zombie_blood.center_x = 375
        zombie_blood.center_y = HEIGHT / 2 + 10

        vial = arcade.Sprite("Chapter 2 Sprites/Vial.png", 0.03)
        vial.center_x = 425
        vial.center_y = HEIGHT / 2 + 10

        antibiotic = arcade.Sprite("Chapter 2 Sprites/Antibiotic.png", 0.03)
        antibiotic.center_x = 475
        antibiotic.center_y = HEIGHT / 2 + 10

        poison = arcade.Sprite("Chapter 2 Sprites/poison.png", 0.2)
        poison.center_x = 525
        poison.center_y = HEIGHT / 2 + 10

        spike = arcade.Sprite("Chapter 2 Sprites/spike.png", 0.2)
        spike.center_x = 550
        spike.center_y = 200

        boulder = arcade.Sprite("Chapter 2 Sprites/boulder.png", 0.03)
        boulder.center_x = 600
        boulder.center_y = 200

        bullet = arcade.Sprite("Chapter 2 Sprites/bullet2.png", 0.3)
        bullet.center_x = 700
        bullet.center_y = 200

        zombie = arcade.Sprite("Chapter 2 Sprites/zombie.png", 0.3)
        zombie.center_x = 500
        zombie.center_y = 200

        gun = arcade.Sprite("Chapter 2 Sprites/raygun.png", 0.2)
        gun.center_x = 600
        gun.center_y = 100

        self.item_list.append(zombie_blood)
        self.item_list.append(antibiotic)
        self.item_list.append(vial)
        self.item_list.append(poison)
        self.item_list.append(spike)
        self.item_list.append(boulder)
        self.item_list.append(bullet)
        self.item_list.append(zombie)
        self.item_list.append(gun)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions", WIDTH / 2, 530,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, 470,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Your task is to collect these:", 50, HEIGHT / 2,
                         arcade.color.WHITE, font_size=20)
        arcade.draw_text("Touching these will result in instadeath:", 50,
                         HEIGHT / 2 - 100, arcade.color.WHITE, font_size=20)
        arcade.draw_text("Use W to jump, A to move left, D to move right", 50,
                         HEIGHT / 2 + 100, arcade.color.WHITE, font_size=20)
        arcade.draw_text("Use the mouse and aim and destroy to the zombie:",
                         50, HEIGHT / 2 - 200, arcade.color.WHITE, font_size=20
                         )

        self.item_list.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Chapter2View()
        game_view.director = self.director
        self.window.show_view(game_view)


class WinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("YOU WIN!", WIDTH / 2, 530,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press space for the next minigame!", WIDTH / 2, 370,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Click to play again!", WIDTH / 2, 470,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Chapter2View()
        game_view.director = self.director
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 240, 400, arcade.color.BLACK, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.BLACK, 24)
        arcade.draw_text("Click to SPACE for next minigame", 200, 200,
                         arcade.color.BLACK, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Chapter2View()
        game_view.director = self.director
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.director.next_view()


class Boulder(arcade.Sprite):
    def reset_pos(self):
        self.center_y = 280
        self.center_x = random.randrange(100, 600)

    def update(self):
        self.angle += self.change_angle


class Player(arcade.Sprite):
    def update(self):
        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH - 1:
            self.right = WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1


class Chapter2View(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.WHITE)

        self.physics_engine = None
        self.time = 30.00
        self.frame_count = 0
        self.player_list = arcade.SpriteList()
        self.player = Player("Chapter 2 Sprites/player.png", 0.02)
        self.player.center_x = 100
        self.player.center_y = 100

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ladder_list = arcade.SpriteList()
        self.death_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player, self.wall_list,
                                           GRAVITY, ladders=self.ladder_list)
        self.boulder = Boulder("Chapter 2 Sprites/boulder.png", 0.03)
        self.boulder.angle = random.randrange(360)
        self.boulder.change_angle = random.randrange(-10, 10)
        self.death_list.append(self.boulder)

        self.zombie = arcade.Sprite("Chapter 2 Sprites/zombie.png", 0.3)
        self.zombie_health = 12
        self.water_gun = arcade.Sprite("Chapter 2 Sprites/raygun.png", 0.15)
        self.background = arcade.Sprite("Chapter 2 Sprites/background.jpg", 1,
                                        center_y=500, center_x=500)

    def on_draw(self):
        arcade.start_render()

        self.background.draw()

        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        output = ("Time: {}: {}".format(minutes, seconds))
        arcade.draw_text(output, WIDTH - 175, HEIGHT - 30, arcade.color.BLACK,
                         24)

        self.player.draw()
        self.item_list.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.death_list.draw()
        self.boulder.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.water_gun not in self.item_list:
            bullet_speed = 30
            bullet = arcade.Sprite('Chapter 2 Sprites/bullet1.png', scale=0.2)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y

            x_diff = x - bullet.center_x
            y_diff = y - bullet.center_y
            angle = math.atan2(y_diff, x_diff)

            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * bullet_speed
            bullet.change_y = math.sin(angle) * bullet_speed
            self.player_bullet_list.append(bullet)
        else:
            pass

    def items(self):
        zombie_blood = arcade.Sprite("Chapter 2 Sprites/Blood.png", 0.2)
        zombie_blood.center_x = 730
        zombie_blood.center_y = 30

        vial = arcade.Sprite("Chapter 2 Sprites/Vial.png", 0.03)
        vial.center_x = 75
        vial.center_y = 180

        antibiotic = arcade.Sprite("Chapter 2 Sprites/Antibiotic.png", 0.03)
        antibiotic.center_x = 730
        antibiotic.center_y = 330

        poison = arcade.Sprite("Chapter 2 Sprites/poison.png", 0.2)
        poison.center_x = 75
        poison.center_y = 480

        self.water_gun.center_x = 730
        self.water_gun.center_y = 480

        self.item_list.append(zombie_blood)
        self.item_list.append(antibiotic)
        self.item_list.append(vial)
        self.item_list.append(poison)
        self.item_list.append(self.water_gun)

    def walls(self):
        for y in range(0, 600, 150):
            if y == 150 or y == 450:
                for x in range(0, 710, 64):
                    wall = arcade.Sprite("Chapter 2 Sprites/floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
            elif y == 300 or y == 600:
                for x in range(100, 800, 64):
                    wall = arcade.Sprite("Chapter 2 Sprites/floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
            else:
                for x in range(0, 800, 64):
                    wall = arcade.Sprite("Chapter 2 Sprites/floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        for y in range(90, 391, 300):
            ladder = arcade.Sprite("Chapter 2 Sprites/ladder.png", 0.30)
            ladder.center_x = 784
            ladder.center_y = y
            self.ladder_list.append(ladder)

        ladder_2 = arcade.Sprite("Chapter 2 Sprites/ladder.png", 0.30)
        ladder_2.center_x = 16
        ladder_2.center_y = 240
        self.ladder_list.append(ladder_2)

    def obstacles(self):
        for x in range(150, 750, 150):
            spike = arcade.Sprite("Chapter 2 Sprites/spike.png", 0.2)
            spike.center_x = x
            spike.center_y = 20
            self.death_list.append(spike)

        for x in range(200, 800, 200):
            platform = arcade.Sprite("Chapter 2 Sprites/Platform.png", 0.3)
            platform.center_y = random.randrange(250, 450)
            platform.center_x = x
            platform.boundary_top = 450
            platform.boundary_bottom = 300
            platform.change_y = - 0.7
            self.death_list.append(platform)
            self.wall_list.append(platform)

        self.zombie.center_x = 120
        self.zombie.center_y = 480
        self.death_list.append(self.zombie)

    def on_show(self):
        self.items()
        self.walls()
        self.obstacles()

    def update(self, delta_time):
        self.time -= delta_time

        self.player.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

        self.boulder.center_y -= 2
        if self.boulder.center_y <= 180:
            self.boulder.reset_pos()

        self.enemy_bullet_list.update()
        self.death_list.update()
        self.player.update()
        self.physics_engine.update()
        self.item_list.update()
        self.player_bullet_list.update()

        self.collisions()
        self.zombie_shoot()

        if len(self.item_list) == 0:
            game_win = WinView()
            game_win.director = self.director
            self.window.show_view(game_win)

    def collisions(self):
        item_hit_list = arcade.check_for_collision_with_list(self.player,
                                                             self.item_list)
        for item in item_hit_list:
            self.item_list.remove(item)

        if arcade.check_for_collision_with_list(
                self.player, self.death_list) or self.time < 0:
            game_over_view = GameOverView()
            game_over_view.director = self.director
            self.window.show_view(game_over_view)

        zombie_hit = arcade.check_for_collision_with_list(
            self.zombie,
            self.player_bullet_list)
        if zombie_hit:
            self.zombie_health -= 1
        for item in zombie_hit:
            self.player_bullet_list.remove(item)
            if self.zombie_health == 0:
                self.zombie.kill()

    def zombie_shoot(self):
        self.frame_count += 1
        if self.zombie in self.death_list:
            if self.frame_count % 120 == 0:
                bullet = arcade.Sprite("Chapter 2 Sprites/bullet2.png", 0.2)
                bullet.center_x = self.zombie.center_x
                bullet.angle = 0
                bullet.top = self.zombie.bottom + 50
                bullet.change_x = 2
                self.enemy_bullet_list.append(bullet)
                self.death_list.append(bullet)


if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(WIDTH, HEIGHT)
    menu_view = Start()
    window.show_view(menu_view)
    my_view = menu_view
    window.show_view(my_view)
    arcade.run()
