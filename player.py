import pyxel
import game_object
import math
import time

class Player(game_object.GameObject):
    def __init__(self):
        super().__init__()
        self.is_airborn = False
        self.is_jumping = False
        self.is_facing_right = True
        self.acceleration = 1
        self.x = 8 * 2
        self.y = 8 * 2
        self.width = 8
        self.height = 8
        self.dx = 0
        self.dy = 0
        self.text = ""

    def update(self):
        tilemap = pyxel.tilemap(0)

        if pyxel.btn(pyxel.KEY_SPACE):
            self.jump()
        if pyxel.btn(pyxel.KEY_LEFT):
            self.accelerate(-1)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.accelerate(1)
        else:
            self.dx = 0


        # should we add gravity?
        if (self.experiencing_gravity(tilemap)):
            self.dy += self.acceleration
            self.is_airborn = False

        if (self.dy > 5):
            self.dy = 5

        if (pyxel.btn(pyxel.KEY_X)) and (self.jumping == False):
            self.jump()

        x = self.x + (self.acceleration * self.dx)
        y = self.y + (self.acceleration * self.dy)

        # handle player clipping with tilemap
        left = math.floor((self.x) / 8)
        right = math.floor((self.x + self.width - 1) / 8)
        top = math.floor(self.y / 8)
        bottom = math.floor((self.y + self.height - 1) / 8)

        new_left = math.floor(x / 8)
        new_right = math.floor((x + 7) / 8)
        new_top = math.floor(y / 8)
        new_bottom = math.floor((y + 7) / 8)

        # x axis checks
        new_x_collides = [
            tilemap.get(new_left, top) != 2,
            tilemap.get(new_right, top) != 2,
            tilemap.get(new_right, bottom) != 2,
            tilemap.get(new_left, bottom) != 2
        ]

        # y axis checks
        new_y_collides = [
            tilemap.get(left, new_top) != 2,
            tilemap.get(right, new_top) != 2,
            tilemap.get(right, new_bottom) != 2,
            tilemap.get(left, new_bottom) != 2
        ]

        # y axis checks
        top_left_tile = tilemap.get(new_left, new_top)
        top_right_tile = tilemap.get(new_right, new_top)
        bottom_left_tile = tilemap.get(new_left, new_bottom)
        bottom_right_tile = tilemap.get(new_right, new_bottom)

        top_left_collide = top_left_tile != 2
        top_right_collide = top_right_tile != 2
        bottom_left_collide = bottom_left_tile != 2
        bottom_right_collide = bottom_right_tile != 2

        # if moving right
        if (self.dx > 0):
            # check if clear
            if not new_x_collides[1] and not new_x_collides[2]:
                self.x = x
            # bottom right only
            elif new_x_collides[2] and not new_x_collides[1] and not new_x_collides[1]:
                self.x = (new_left) * 8
                self.dx = 0
            # both right
            elif new_x_collides[1] and new_x_collides[2]:
                self.x = (new_left) * 8
                self.dx = 0
            else:
                self.dx = 0

        # if moving left
        if (self.dx < 0):
            # check if clear
            if not new_x_collides[0] and not new_x_collides[3]:
                self.x = x
            # bottom left only
            elif new_x_collides[3] and not new_x_collides[0] and not new_x_collides[2]:
                self.x = new_right * 8
                self.dx = 0
            # top left only
            elif new_x_collides[0] and not new_x_collides[2] and new_x_collides[3]:
                self.x = new_right * 8
                self.dx = 0
            else:
                self.dx = 0

        # if moving down
        if (self.dy > 0):
            # check if clear
            if not new_y_collides[3] and not new_y_collides[2]:
                self.y = y
            # both lefts
            elif new_y_collides[3] and new_y_collides[0] and not new_y_collides[2]:
                self.y = y
            # both rights
            elif new_y_collides[2] and new_y_collides[1] and not new_y_collides[3]:
                self.y = y
            elif new_y_collides[3] and not new_y_collides[2]:
                # bottom left only
                self.y = new_top * 8
                self.dy = 0
            elif new_y_collides[3] and not new_y_collides[2]:
                self.y = new_top * 8
                self.dy = 0
            # bottom right only
            elif new_y_collides[2] and not new_y_collides[3]:
                self.y = new_top * 8
                self.dy = 0
            else:
                self.dy = 0

        # if moving up
        if (self.dy < 0):
            # check if clear
            if not new_y_collides[0] and not new_y_collides[1]:
                self.y = y
            # top left only
            elif new_y_collides[0] and not new_y_collides[1]:
                self.y = (new_bottom - 1) * 8
                self.dy = 0
            # top right only
            elif new_y_collides[1] and not new_y_collides[0]:
                self.y = (new_bottom - 1) * 8
                self.dy = 0
            else:
                self.dy = 0

    def experiencing_gravity(self, tilemap):
        left = math.floor(self.x / 8)
        right = math.floor((self.x + 7) / 8)
        below = math.floor((self.y + 8) / 8)

        tile_below_left = tilemap.get(left, below)
        tile_below_right = tilemap.get(right, below)

        if (tile_below_left == 2) and (tile_below_right == 2):
            return True
        self.is_jumping = False
        return False

    def jump(self):
        if (not self.is_airborn) and not(self.is_jumping):
            self.is_airborn = True
            self.is_jumping = True
            self.dy = -8

    def accelerate(self, diff):
        max_dx = 2
        new = self.dx + diff
        if (new > max_dx):
            self.dx = max_dx
        elif (new < max_dx * -1):
            self.dx = max_dx * -1
        else:
            self.dx = new

