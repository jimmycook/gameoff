import pyxel

import player

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("resources.pyxel")

        self.player = player.Player()

        self.platforms = []

        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit the game of Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # update the player
        self.player.update()

    def draw(self):
        pyxel.cls(0)

        # Draw the tilemap
        pyxel.bltm(0, 0, 0, 0, 0, 0, 50, 50)

        # Player sprite direction
        width = self.player.width
        if not self.player.is_facing_right:
            width = width * -1

        pyxel.blt(self.player.x, self.player.y, 0, 0, 0, width, self.player.height, 0)
        pyxel.text(2, 2, self.player.text, 7)

App()
