import arcade

import warnings
warnings.filterwarnings("ignore")

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 560
WINDOW_TITLE = "GO JUST GO"
PLAYER_SPEED = 1.5
ANIMATE_SPEED = 10

class GameView(arcade.Window):

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_texture=None
        self.player_texture_r = None
        self.player_texture_l = None
        self.player_texture_up = None
        self.player_sprite=None
        self.player_list=None
        self.tiled_map=None
        self.scene=None

        self.camera = None
        self.current_map = 1

        self.key_right_pressed=False
        self.key_left_pressed=False
        self.key_up_pressed=False
        self.key_down_pressed=False

        self.wall_list = None

        self.last_key = None

        self.player_animate_r = []
        self.player_animate_l = []
        self.player_animate_up = []
        self.player_animate_down = []

        self.npc_list = None
        self.npc_textures = []
        self.npc_frame_counter = 0

        self.weapon_textures = []
        self.weapon_list = None
        self.weapon_frame_counter = 0
        self.weapon_collected = False

        self.bullet_list = arcade.SpriteList()
        self.bullet_texture = None
        self.bullet_texture2 = None
        self.bullet_speed = 10
        self.last_move_direction = ""

        self.start_text = True
        self.game_dea = False
        self.game_over = False


    def setup(self):

        self.player_texture = arcade.load_texture("character/back0.png")
        self.player_texture_l = arcade.load_texture("character/left1.png")
        self.player_texture_r = arcade.load_texture("character/right1.png")
        self.player_texture_up = arcade.load_texture("character/forward0.png")
        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.14)

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        if self.current_map == 1:
            self.tiled_map = arcade.load_tilemap("map1x2/map1.tmj", scaling=0.5)
            self.player_sprite.center_x = 380
            self.player_sprite.center_y = 210

        elif self.current_map == 2:
            self.tiled_map = arcade.load_tilemap("map2/mapa.tmj", scaling=0.4)
            self.player_sprite.center_x = 115
            self.player_sprite.center_y = 100

        elif self.current_map == 3:
            self.tiled_map = arcade.load_tilemap("map2/mapp/mapp2.tmj", scaling=0.4)
            self.player_sprite.center_x = 750
            self.player_sprite.center_y = 100

        elif self.current_map == 4:
            self.tiled_map = arcade.load_tilemap("map3/tld/3.2.tmj", scaling=0.4)
            self.player_sprite.center_x = 120
            self.player_sprite.center_y = 200

            for i in range(1, 5):
                texture = arcade.load_texture(f"map3/character/npc{i}.png")
                self.npc_textures.append(texture)

            self.npc_list = arcade.SpriteList()

            npc_positions = [(240, 200), (480, 250), (785, 200)]
            for i in npc_positions:
                npc = arcade.Sprite(self.npc_textures[0], scale=0.9)
                npc.center_x = i[0]
                npc.center_y = i[1]
                self.npc_list.append(npc)

            self.weapon_textures = [
                arcade.load_texture("map3/character/weapon1.png"),
                arcade.load_texture("map3/character/weapon2.png")
            ]

            self.weapon_list = arcade.SpriteList()

            weapon = arcade.Sprite(self.weapon_textures[0], scale=0.05)
            weapon.center_x = 80
            weapon.center_y = 220
            self.weapon_list.append(weapon)

            self.bullet_texture = arcade.load_texture("map3/character/bullet.png")
            self.bullet_texture2 = arcade.load_texture("map3/character/bullet2.png")
            self.bullet_list = arcade.SpriteList()

        elif self.current_map == 5:
            self.tiled_map = arcade.load_tilemap("map4/111.tmj", scaling=0.5)
            self.player_sprite.scale = 0.3
            self.player_sprite.center_x = 321
            self.player_sprite.center_y = 129


        self.scene = arcade.Scene.from_tilemap(self.tiled_map)

        self.camera = arcade.Camera2D()

        self.background_color = arcade.csscolor.BLACK


        self.wall_list = self.scene.get_sprite_list("1.5")

        self.player_animate_r = []
        self.player_animate_l = []
        self.player_animate_up = []
        self.player_animate_down = []

        for i in range(1,3):
            self.player_animate_r.append(arcade.load_texture(f"character/right{i}.png"))
            self.player_animate_l.append(arcade.load_texture(f"character/left{i}.png"))
            self.player_animate_up.append(arcade.load_texture(f"character/forward{i}.png"))
            self.player_animate_down.append(arcade.load_texture(f"character/back{i}.png"))


    def on_draw(self):

        self.clear()

        self.camera.use()

        self.scene.draw()

        if self.current_map == 4 and not self.weapon_collected:
            self.weapon_list.draw()

        self.player_list.draw()

        if self.current_map == 4:
            self.npc_list.draw()

        self.scene["2.0"].draw()

        self.bullet_list.draw()

        if self.start_text:
            arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, (0, 0, 0, 220))
            arcade.draw_text("press Enter to start", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.WHITE, font_size=40, font_name="Silver", anchor_x="center", anchor_y="center")

        if self.game_dea:
            arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, (0, 0, 0, 220))
            arcade.draw_text("You died", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.WHITE, font_size=40, font_name="Silver", anchor_x="center", anchor_y="center")
            arcade.draw_text("press escape", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 -40, arcade.color.WHITE, font_size=40, font_name="Silver", anchor_x="center", anchor_y="center")

        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, (0, 0, 0, 220))
            arcade.draw_text("Game over", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.WHITE, font_size=40, font_name="Silver", anchor_x="center", anchor_y="center")
            arcade.draw_text("press escape", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40, arcade.color.WHITE, font_size=40, font_name="Silver", anchor_x="center", anchor_y="center")


    def center_camera_player1(self):

        map_width = self.tiled_map.width * self.tiled_map.tile_width * self.tiled_map.scaling
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.camera.viewport_height / 2 -24

        if screen_center_x <  self.tiled_map.tile_width *4.6:
            screen_center_x = self.camera.viewport_width / 2 -32

        if screen_center_x > map_width - self.tiled_map.tile_width *4.6:
            screen_center_x = map_width - self.camera.viewport_width / 2 + 32


        self.camera.position = screen_center_x, screen_center_y

    def collision_walls(self, dx=0, dy=0):

        next_left = self.player_sprite.center_x - self.player_sprite.width / 2 + dx
        next_right = self.player_sprite.center_x + self.player_sprite.width / 2 + dx

        if self.current_map == 1 and (160 < self.player_sprite.center_x < 320 and 390 < self.player_sprite.center_y < 450):
            next_bottom = self.player_sprite.center_y -18 + dy
            next_top = self.player_sprite.center_y +8 + dy
        elif self.current_map == 1 and (80 < self.player_sprite.center_x < 440 and 280 < self.player_sprite.center_y < 360):
            next_bottom = self.player_sprite.center_y - self.player_sprite.height / 2 - 5 + dy
            next_top = self.player_sprite.center_y - self.player_sprite.height / 2 + 33 + dy

        elif self.current_map == 1 and (553 < self.player_sprite.center_x < 560 and 200 < self.player_sprite.center_y < 320):
            next_bottom = self.player_sprite.center_y - self.player_sprite.height / 2 - 5 + dy
            next_top = self.player_sprite.center_y - self.player_sprite.height / 2 + dy
        elif self.current_map == 4 and (330 < self.player_sprite.center_x < 640):
            next_bottom = self.player_sprite.center_y - self.player_sprite.height / 2 -22  + dy
            next_top = self.player_sprite.center_y - self.player_sprite.height / 2 +30 + dy
        else:
            next_bottom = self.player_sprite.center_y - self.player_sprite.height / 2 - 5 + dy
            next_top = self.player_sprite.center_y - self.player_sprite.height / 2 + 25 + dy

        for block in self.wall_list:
            block_left = block.center_x - block.width / 2
            block_right = block.center_x + block.width / 2
            block_bottom = block.center_y - block.height / 2
            block_top = block.center_y + block.height / 2

            if next_right > block_left and next_left < block_right and \
                    next_top > block_bottom and next_bottom < block_top:
                return True
        return False

    def player_movement(self):

        if self.start_text or self.game_dea or self.game_over:
            return

        dx = 0
        dy = 0

        if self.last_key == arcade.key.W:
            dy = PLAYER_SPEED
            self.player_sprite.texture = self.player_animate_up[int(self.player_sprite.center_y / ANIMATE_SPEED) % 2]
            self.last_move_direction = "left"
        elif self.last_key == arcade.key.S:
            dy = -PLAYER_SPEED
            self.player_sprite.texture = self.player_animate_down[int(self.player_sprite.center_y/ ANIMATE_SPEED) % 2]
            self.last_move_direction = "right"
        elif self.last_key == arcade.key.A:
            dx = -PLAYER_SPEED
            self.player_sprite.texture = self.player_animate_l[int(self.player_sprite.center_x / ANIMATE_SPEED) % 2]
            self.last_move_direction = "left"
        elif self.last_key == arcade.key.D:
            dx = PLAYER_SPEED
            self.player_sprite.texture = self.player_animate_r[int(self.player_sprite.center_x/ANIMATE_SPEED)%2]
            self.last_move_direction = "right"

        if self.collision_walls(dx=dx, dy=0):
            self.player_sprite.center_x -= dx
            dx = -dx
        else:
            self.player_sprite.center_x += dx

        if self.collision_walls(dx=0, dy=dy):
            self.player_sprite.center_y -= dy
            dy = -dy
        else:
            self.player_sprite.center_y += dy

    def check_npc_bullet(self):
        if self.current_map == 4 and self.npc_list and self.bullet_list:
            for bullet in self.bullet_list:
                bullet_left = bullet.center_x - bullet.width / 2
                bullet_right = bullet.center_x + bullet.width / 2
                bullet_bottom = bullet.center_y - bullet.height / 2
                bullet_top = bullet.center_y + bullet.height / 2

                if (bullet.center_x < 0 or bullet.center_x > WINDOW_WIDTH or
                        bullet.center_y < 0 or bullet.center_y > WINDOW_HEIGHT):
                    bullet.remove_from_sprite_lists()

                for npc in self.npc_list:
                    npc_left = npc.center_x - npc.width / 2
                    npc_right = npc.center_x + npc.width / 2
                    npc_bottom = npc.center_y - npc.height / 2
                    npc_top = npc.center_y + npc.height / 2

                    if bullet_right > npc_left and bullet_left < npc_right and \
                            bullet_top > npc_bottom and bullet_bottom < npc_top:

                        npc.remove_from_sprite_lists()
                        bullet.remove_from_sprite_lists()


    def check_npc_player(self):
        if self.current_map == 4 and self.npc_list:
            for npc in self.npc_list:
                npc_left = npc.center_x - npc.width / 2
                npc_right = npc.center_x + npc.width / 2
                npc_bottom = npc.center_y - npc.height / 2
                npc_top = npc.center_y + npc.height / 2

                player_left = self.player_sprite.center_x - self.player_sprite.width / 2
                player_right = self.player_sprite.center_x + self.player_sprite.width / 2
                player_bottom = self.player_sprite.center_y - self.player_sprite.height / 2
                player_top = self.player_sprite.center_y + self.player_sprite.height / 2

                if player_right > npc_left and player_left < npc_right and \
                   player_top > npc_bottom and player_bottom < npc_top:
                    self.game_dea = True


    def on_update(self, delta_time):

        if self.current_map == 1 or self.current_map == 5:
            self.camera.position = (self.camera.viewport_width / 2, self.camera.viewport_height / 2)

        if self.current_map > 1 and self.current_map != 3 and self.current_map != 5:
            self.center_camera_player1()

        if self.current_map == 3:
            self.camera.position = self.player_sprite.center_x, self.player_sprite.center_y +155

        if self.current_map == 2 and self.player_sprite.center_x > 750:
            self.current_map = 3
            self.setup()

        self.player_movement()

        self.bullet_list.update()

        if self.current_map == 4:
            self.npc_frame_counter += 1
            current_frame = (self.npc_frame_counter // 10) % len(self.npc_textures)
            for i in self.npc_list:
                i.texture = self.npc_textures[current_frame]

        if self.current_map == 4 and not self.weapon_collected:
            self.weapon_frame_counter += 1
            current_frame = (self.weapon_frame_counter // 20) % len(self.weapon_textures)
            for weapon in self.weapon_list:
                weapon.texture = self.weapon_textures[current_frame]

        self.check_npc_bullet()
        self.check_npc_player()

        if self.current_map == 5:
            min_y = 126
            max_y = 500
            min_scale = 0.08
            max_scale = 0.3

            self.player_sprite.center_y = min(self.player_sprite.center_y, max_y)

            t = (self.player_sprite.center_y - min_y) / (max_y - min_y)
            self.player_sprite.scale = max_scale - (max_scale - min_scale) * t
            if  self.player_sprite.center_y> 465:
                self.game_over = True

        #print(self.player_sprite.center_x, self.player_sprite.center_y)

    def weapon(self, key):
        if key == arcade.key.E and self.current_map == 4 and not self.weapon_collected:
            for weapon in self.weapon_list:
                if 80 < self.player_sprite.center_x < 100 and 200 < self.player_sprite.center_y:
                    self.weapon_collected = True
                    weapon.remove_from_sprite_lists()

                    self.player_texture = arcade.load_texture("map3/character/111/back0.png")
                    self.player_texture_l = arcade.load_texture("map3/character/111/left1.png")
                    self.player_texture_r = arcade.load_texture("map3/character/111/right1.png")
                    self.player_texture_up = arcade.load_texture("map3/character/111/forward0.png")

                    self.player_animate_r = []
                    self.player_animate_l = []
                    self.player_animate_up = []
                    self.player_animate_down = []

                    for i in range(1, 3):
                        self.player_animate_r.append(arcade.load_texture(f"map3/character/111/right{i}.png"))
                        self.player_animate_l.append(arcade.load_texture(f"map3/character/111/left{i}.png"))
                        self.player_animate_up.append(arcade.load_texture(f"map3/character/111/forward{i}.png"))
                        self.player_animate_down.append(arcade.load_texture(f"map3/character/111/back{i}.png"))
                break


    def on_key_press(self, key, modifiers):

        if key == arcade.key.ENTER:
            self.start_text = False

        if key == arcade.key.ESCAPE:
            self.current_map = 1
            self.start_text = True
            self.game_dea = False
            self.game_over = False
            self.weapon_collected = False
            self.setup()


        if key == arcade.key.E and self.current_map == 1:
            if 360 < self.player_sprite.center_x < 440 and 280 < self.player_sprite.center_y < 360:
                self.player_sprite.position = (290, 425)

            if 290 < self.player_sprite.center_x < 320 and 390 < self.player_sprite.center_y < 450:
                self.player_sprite.position = (380, 320)

            if 215 < self.player_sprite.center_x < 285 and 415 < self.player_sprite.center_y < 435:
                self.current_map = 2
                self.setup()


        if key == arcade.key.E and self.current_map == 3:
            if 1480 < self.player_sprite.center_x < 1530 and 670 < self.player_sprite.center_y < 706:
                self.current_map = 4
                self.setup()


        if key == arcade.key.E and self.current_map == 4:
            if 279 < self.player_sprite.center_x < 299 and 190 < self.player_sprite.center_y:
                self.player_sprite.position = (392, 260)
            if 373 < self.player_sprite.center_x < 392:
                self.player_sprite.position = (265, 220)
            if 566 < self.player_sprite.center_x < 586:
                self.player_sprite.position = (682, 220)
            if 662 < self.player_sprite.center_x < 682 and 190 < self.player_sprite.center_y:
                self.player_sprite.position = (566, 260)
            if 870 < self.player_sprite.center_x < 893 and 210 < self.player_sprite.center_y:
                self.current_map = 5
                self.setup()

        if key == arcade.key.W:
            self.key_up_pressed = True
        elif key == arcade.key.S:
            self.key_down_pressed = True
        elif key == arcade.key.A:
            self.key_left_pressed = True
        elif key == arcade.key.D:
            self.key_right_pressed = True

        if key in (arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D):
            self.last_key = key

        self.weapon(key)

        if key == arcade.key.R and self.current_map == 4 and self.weapon_collected:


            if self.last_move_direction == "right":
                bullet = arcade.Sprite(self.bullet_texture, scale=0.04)
                bullet.center_x = self.player_sprite.center_x +20
                bullet.center_y = self.player_sprite.center_y -20
                bullet.change_x = self.bullet_speed
                bullet.change_y = 0
            elif self.last_move_direction == "left":
                bullet = arcade.Sprite(self.bullet_texture2, scale=0.04)
                bullet.center_x = self.player_sprite.center_x -20
                bullet.center_y = self.player_sprite.center_y -20
                bullet.change_x = -self.bullet_speed
                bullet.change_y = 0
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W:
            self.key_up_pressed= False
            self.player_sprite.texture = self.player_texture_up
        elif key == arcade.key.S:
            self.key_down_pressed= False
            self.player_sprite.texture = self.player_texture
        elif key == arcade.key.A:
             self.key_left_pressed= False
             self.player_sprite.texture = self.player_texture_l
        elif key == arcade.key.D:
            self.key_right_pressed= False
            self.player_sprite.texture = self.player_texture_r

        if self.last_key == key:
            self.last_key = None


def main():

    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()