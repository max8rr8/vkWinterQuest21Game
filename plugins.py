import game_map
import solution

class Plugin:
  def render(self, game, img):
    pass

  def click(self, game, x, y):
    pass

  def keypress(self, game, key):
    pass

class PositionPlugin(Plugin):
  def render(self, game, img):
    cords, _ = game.execState
    img.setCellCenter(cords[0], cords[1], (0, 0, 255))

class ManualMovementPlugin(Plugin):
  state = "idle"

  def keypress(self, game, key):
    if key == ord('n'):
      if self.state == "idle":
        self.state = "select"
      else:
        self.state = "idle"
      game.render()

  def render(self, game, img):
    if self.state == "idle": return

    cords, vector = game.execState
    cx, cy = cords
    vx, vy = vector

    lim = -1
    if game_map.NUMPY_MAP[cx, cy] == game_map.SNOW: lim = 1
    if game_map.NUMPY_MAP[cx, cy] == game_map.ICE: lim = 2

    for dx in range(-2, 3, 1):
      for dy in range(-2, 3, 1):
        col = (0, 127, 255)

        if abs(dx) <= lim and abs(dy) <= lim:
          col = (127, 0, 255)

        if dx == 0 and dy == 0:
          col = (255, 0, 255)

        img.setCellCenter(cx + vx + dx, cy + vy + dy, col)

  def click(self, game, x, y):
    print("click", self.state)
    if self.state == "idle": return

    cords, vector = game.execState
    cx, cy = cords
    vx, vy = vector

    dx = x - cx - vx
    dy = y - cy - vy

    print(x, y, cx, cy, vx, vy)

    if abs(dx) > 2 or abs(dy) > 2:
      print("Wrong move")
      self.state = "idle"
      game.render()
      return

    game.append_cmd([(dx, dy)])

class CmdRollbackPlugin(Plugin):
  def keypress(self, game, key):
    if key == ord('m'):
      game.set_cmd(game.cmds[:-1])

class MarkedPresentsPlugin(Plugin):
  def render(self, game, img):
    for present in game.presents:
      img.setFullCell(present[0], present[1], (0, 255, 255))
    
class SaveLoadPlugin(Plugin):
  saved_cmds = []

  def keypress(self, game, key):
    if key == ord('k'):
      self.saved_cmds = game.cmds.copy()    
    if key == ord('l'):
      game.set_cmd(self.saved_cmds.copy())

class ExportPlugin(Plugin):
  def keypress(self, game, key):
    if key == ord('s'):
      print(game.cmds)
      solution.save_solution(game.cmds, game.upgrades)