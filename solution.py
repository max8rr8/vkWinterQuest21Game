import json
def save_solution(cmd, to_upgrade):
  path = []
  vx, vy = 0, 0
  cx, cy = 0, 0
  px, py = cx, cy
  for x, y in cmd:
    vx += x
    vy += y
    cx += vx
    cy += vy
    path.append((cy - py, cx - px))
    px, py = cx, cy

  tes = {"job": [[y, x] for x,y in to_upgrade], "path": path}

  with open("solution.json", "w") as f:
    json.dump(tes, f)