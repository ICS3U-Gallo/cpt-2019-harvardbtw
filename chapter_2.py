import arcade

WIDTH = 1000
HEIGHT = 1000
MOVEMENT_SPEED = 4
GRAVITY = 1
PLAYER_JUMP_SPEED = 15
SLOW = 2.5


class Room:
    pass


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


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.physics_engine = None
        self.time = 30.00

        self.player_list = arcade.SpriteList()
        self.player = Player("zerotwo.jpg", 0.05)
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

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY,
                                                             ladders=self.ladder_list)

    def on_draw(self):
        arcade.start_render()

        minutes = int(self.time) // 60
        seconds = int(self.time) % 60
        output = ("Time: {}: {}".format(minutes, seconds))
        arcade.draw_text(output, WIDTH - 175, HEIGHT - 30, arcade.color.BLACK, 24)

        self.player.draw()
        self.item_list.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.death_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
            self.up_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def update(self, delta_time):
        self.time -= delta_time
        self.player.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

        self.player.update()
        self.physics_engine.update()
        self.item_list.update()

        item_hit_list = arcade.check_for_collision_with_list(self.player, self.item_list)
        for item in item_hit_list:
            item.remove_from_sprite_lists()

    def on_show(self):
        zombie_blood = arcade.Sprite("Blood.png", 0.2)
        zombie_blood.center_x = 930
        zombie_blood.center_y = 40

        vial = arcade.Sprite("Vial.png", 0.03)
        vial.center_x = 75
        vial.center_y = 240

        antibiotic = arcade.Sprite("Antibiotic.png", 0.03)
        antibiotic.center_x = 930
        antibiotic.center_y = 440

        poison = arcade.Sprite("poison.jpg", 0.2)
        poison.center_x = 75
        poison.center_y = 640

        self.item_list.append(zombie_blood)
        self.item_list.append(antibiotic)
        self.item_list.append(vial)
        self.item_list.append(poison)

        for y in range(10, 1010, 200):
            if y == 210 or y == 610:
                for x in range(0, 900, 64):
                    wall = arcade.Sprite("floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
            elif y == 410 or y == 810:
                for x in range(100, 1000, 64):
                    wall = arcade.Sprite("floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
            else:
                for x in range(0, 1000, 64):
                    wall = arcade.Sprite("floor.png", 0.06)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        for y in range(118, 618, 400):
            ladder = arcade.Sprite("ladder.png", 0.35)
            ladder.center_x = 980
            ladder.center_y = y
            self.ladder_list.append(ladder)

        for y in range(318, 817, 400):
            ladder_2 = arcade.Sprite("ladder.png", 0.35)
            ladder_2.center_x = 20
            ladder_2.center_y = y
            self.ladder_list.append(ladder_2)

        for x in range(150, 900, 150):
            spike = arcade.Sprite("spike.png", 0.2)
            spike.center_x = x
            spike.center_y = 33
            self.death_list.append(spike)


if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT)
    my_view = Chapter1View()
    window.show_view(my_view)
    arcade.run()
