import game_map
import executor
import numpy as np
import cv2


colors = np.zeros((11, 3))
colors[game_map.WALL] = (0, 0, 0)
colors[game_map.DROP] = (0, 255, 0)
colors[game_map.SNOW] = (255, 255, 255)
colors[game_map.ICE] = (255, 0, 0)
colors[game_map.ROAD] = (128, 128, 128)


class Image:
  def __init__(self):
    self.img = colors[game_map.NUMPY_MAP]
    self.img = np.repeat(self.img, 8, axis=0)
    self.img = np.repeat(self.img, 8, axis=1)
    self.img = self.img.astype(np.uint8)
    for ix in range(7, 800, 8):
      self.img[:, ix] = (64, 64, 64)
    for iy in range(7, 800, 8):
      self.img[iy, :] = (64, 64, 64)

  def setCellCenter(self, x, y, color):
    self.img[x * 8 + 2:x * 8 + 5, y * 8 + 2:y * 8 + 5] = color


  def setFullCell(self, x, y, color):
    self.img[x * 8:x * 8 + 7, y * 8:y * 8 + 7] = color




class Game:
  def __init__(self):
    self.cmds = []
    self.plugins = []
    self.compute()

  def compute(self):
    self.presents, self.execState, self.upgrades = executor.simple_executor(self.cmds)
    self.score = executor.score(len(self.presents), len(self.cmds), len(self.upgrades))
    self.render()

    print("Score", self.score)
    print("Presents left", 176 - len(self.presents))
    print("Commands length", len(self.cmds))
    print("Upgrades", len(self.upgrades))


  def set_cmd(self, cmds):
    self.cmds = cmds
    self.compute()

  def append_cmd(self, cmds):
    self.cmds += cmds
    self.compute()

  def render(self):
    self.img = Image()
    for plugin in self.plugins:
      plugin.render(self, self.img)

  def click_handler(self, event, y, x, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
      for plugin in self.plugins:
        plugin.click(self, x // 8, y // 8)


  def run(self):
    self.compute()
    cv2.namedWindow('Game')
    cv2.setMouseCallback("Game", self.click_handler)

    while True:
      cv2.imshow("Game", self.img.img)
      k = cv2.waitKey(1) & 0xff
      if k == ord('q'):
        break
      if k != -1:
        for plugin in self.plugins:
          plugin.keypress(self, k)
