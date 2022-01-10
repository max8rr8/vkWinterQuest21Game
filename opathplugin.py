from plugins import Plugin
import time
import executor
import tqdm
from multiprocessing import Pool
import operator


def try_sol(g):
  start_state, cmd = g
  _, st, attempt_upgrades = executor.simple_executor(
      cmd, start_state=start_state)
  if attempt_upgrades is not None:
    cords, v = st
    # if cords[0] == targ_x and cords[1] == targ_y:
    sc = len(attempt_upgrades) + len(cmd) - len(start_state[2])
    return sc
  else:
    return 800

class OptimalPathPlugin(Plugin):
  state="idle"

  target_cords = None
  vector_cords = None

  def keypress(self, game, key):
    if key == ord('x'):
      if self.state == "idle":
        self.state = "select1"
      else:
        self.state = "idle"



  def find_mag(self, delta, st, en):
    v = []
    nv = []
    sol = []

    v.append([])

    good = []

    ct = time.time()
    for i in range(8):
      # print(len(v))
      a = 0
      for k in v:
        if time.time() - ct > 3:
          break
        # a+=1
        # print(a)
        for j in range(-2, 3):
          nv.append(k + [j])

        sp = st
        c = 0
        for h in k:
          sp += h
          c += sp

        if abs(sp - en) < 3 and c == delta:
          good.append(k)
          # print(good)
      # print("good")
      v = nv.copy()
    return good

  def calculate(self, game):
    presents, state, upgrades = executor.simple_executor(game.cmds)

    cx, cy = state[0]
    vx, vy = state[1]

    targ_x, targ_y = self.target_cords

    print("Starting optimal path search")
    mag_x = self.find_mag(targ_x - cx, vx, self.vector_cords[0] - targ_x)
    mag_y = self.find_mag(targ_y - cy, vy, self.vector_cords[1] - targ_y)
    print("Found mags", len(mag_x), len(mag_y))

    best_sc = None
    best_cmd = None

    vap = []

    for mx in tqdm.tqdm(mag_x):
      for my in mag_y:
        if len(mx) == len(my):
          vap.append(list(zip(mx, my)))
    print("Generated", len(vap), "variants")


    for cmd in tqdm.tqdm(vap):
      if best_sc is None or len(cmd) < best_sc:
        _, st, attempt_upgrades = executor.simple_executor(cmd,
                                                          start_state=(*state, upgrades))
        if attempt_upgrades is not None:
          cords, v = st
          sc = len(attempt_upgrades) + len(cmd) - len(upgrades)
          if best_sc is None or sc < best_sc:
            best_sc = sc
            best_cmd = cmd

    # with Pool(12) as p:
    #   scores = list(tqdm.tqdm(p.imap(try_sol, vap), total=len(vap)))
    # best_cmd_i, best_sc = min(enumerate(scores), key=operator.itemgetter(1))
    # if best_sc == 800:
    #   best_cmd = None
    # else:
    #   best_cmd  = vap[best_cmd_i][1]

    print("Found best score:", best_sc)

    if best_cmd is None:
      print("Failed to find a solution")
      # return []
    else:
      game.append_cmd(best_cmd)



  def click(self, game, x, y):
    if self.state == "idle": return
    if self.state == "select1":
      print("Selected target")
      self.target_cords = (x, y)
      self.state = "select2"
    elif self.state == "select2":
      print("Starting computation")
      self.vector_cords = (x, y)
      self.state = "idle"
      self.calculate(game)
