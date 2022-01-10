import game_map

def simple_executor(cmds, start_state=((49, 57), (0, 0), [])):

  cx, cy = start_state[0]
  vx, vy = start_state[1]

  drops = set([])
  via = set([])
  svia = set([])

  for u in start_state[2]:
    if u not in via:
      via.add(u)
    else:
      svia.add(u)

  for i, cmd in enumerate(cmds):
    cmdx, cmdy = cmd
    cradius = game_map.NUMPY_MAP[cx, cy]

    flags = ""
    if abs(cmdx) > cradius or abs(cmdy) > cradius:
      flags += "B"
      via.add((cx, cy))
      if abs(cmdx) > cradius + 1 or abs(cmdy) > cradius + 1:
        flags += "B"
        svia.add((cx, cy))

      # return None, None
    vx += cmdx
    vy += cmdy
    cx += vx
    cy += vy

    if cx > 99: cx = 99
    if cy > 99: cy = 99
    if cx < 0: cx = 0
    if cy < 0: cy = 0


    if game_map.NUMPY_MAP[cx, cy] == game_map.WALL:
      # print("Wall collision", cx, cy, i)
      return None, None, None
    if game_map.NUMPY_MAP[cx, cy] == game_map.DROP:
      flags+="P"
      drops.add((cx, cy))


    # print(f"CORDS\t{cx}\t{cy}\tVECTOR\t{vx}\t{vy}\t{flags}")
  return drops, ((cx,cy), (vx, vy)), list(via) + list(svia)

import numpy as np



def meta_executor(meta_cmds):
  n_sols = len(meta_cmds)

  upd_m = np.zeros((n_sols, 100, 100))
  vect = np.zeros((n_sols, 2), dtype=np.int32)
  vect[:, 0] = 0
  vect[:, 1] = 0

  cords = np.zeros((n_sols, 2), dtype=np.int32)
  cords[:, 0] = 49
  cords[:, 1] = 57

  allvertex = np.arange(0, n_sols)

  presents = np.zeros((n_sols, 177), dtype=np.int32) + 800
  failed = np.zeros((n_sols,), dtype=np.bool)

  for s in range(360):
    # print(allvertex.shape, cords.shape)
    objs = game_map.NUMPY_MAP[cords[:, 0], cords[:, 1]]
    failed[objs == game_map.WALL] = True

    present_idx = game_map.PRESENTS_MAP[cords[:, 0], cords[:, 1]]
    # print(present_idx.dtype, allvertex.dtype)
    presents[allvertex, present_idx] = np.minimum(s,presents[allvertex, present_idx])

    # np.abs(cmdx)

    # print(present_idx)
    vect += meta_cmds[:, s]
    cords += vect
    cords = np.minimum(cords, 100)
    cords = np.maximum(cords, 0)

  presents[presents == 800] = 0
  delivered_presents = np.count_nonzero(presents, axis=1)
  last_cmd = np.max(presents, axis=1) + 1

  # print(delivered_presents, last_cmd)

  score = 3600 * (1.1 ** delivered_presents.astype(np.float32)) / last_cmd.astype(np.float32)
  score[delivered_presents == 0] = 0
  score[failed] = 0

  return score

def check_exec(cmds, sc, ec):
  sx, sy = sc
  ex, ey = ec

  n_sols = len(cmds)

  vect = np.zeros((n_sols, 2), dtype=np.int32)
  vect[:, 0] = 0
  vect[:, 1] = 0

  cords = np.zeros((n_sols, 2), dtype=np.int32)
  cords[:, 0] = sx
  cords[:, 1] = sy

  failed = np.zeros((n_sols, ), dtype=np.bool)

  done = np.zeros((n_sols, ), dtype=np.int32) + 800

  upds = np.zeros((n_sols, ), dtype=np.int32)

  for s in range(80):
    # print(allvertex.shape, cords.shape)
    objs = game_map.NUMPY_MAP[cords[:, 0], cords[:, 1]]
    failed[objs == game_map.WALL] = True

    maxr = np.maximum(np.abs(cmds[:, s, 0]), np.abs(cmds[:, s, 1]))
    up = np.maximum(0, maxr - game_map.MAX_VECTOR_MAP[cords[:, 0], cords[:, 1]])
    upds += up
    # print(cmds)

    vect += cmds[:, s]
    cords += vect
    cords = np.minimum(cords, 99)
    cords = np.maximum(cords, 0)

    k = (vect[:, 0] == 0) & (vect[:, 1] == 0)
    k &= (cords[:, 0] == ex) & (cords[:, 1] == ey)
    done[k] = np.minimum(done[k], s)

  done[failed] = 1000
  done += upds
  # print(done)

  return done

def score(presents, cmd_len, upgrades_len):
  if presents == 0: return 0
  if cmd_len == 0: cmd_len = 1

  return 3600 * (1.1 ** presents) / (cmd_len + upgrades_len)