import json
import numpy as np

WALL = 9
ICE = 0
SNOW = 1
ROAD = 2
START = 3
DROP = 4

NAMES = {
    WALL: "СТЕНА",
    ICE: "ЛЕД",
    SNOW: "СНЕГ",
    ROAD: "ДОРОГА",
    START: "СТАРТ",
    DROP: "ЦЕЛЬ"
}

RADIUS = {WALL: -1, ICE: 0, SNOW: 1, ROAD: 2, DROP: 2, START: 2}

with open("map.json", "r") as f:
  PY_MAP = json.load(f)["raw_map"]

NUMPY_RADIUS = np.array([RADIUS[x] if x in RADIUS else -1 for x in range(10)])
print(NUMPY_RADIUS)

NUMPY_MAP = np.array(PY_MAP, dtype=np.int8)
MAX_VECTOR_MAP = NUMPY_RADIUS[NUMPY_MAP]

PRESENTS = list(zip(*np.where(NUMPY_MAP == DROP)))
PRESENTS_MAP = np.zeros(NUMPY_MAP.shape, dtype=np.int64)
for i, pos in enumerate(PRESENTS):
  PRESENTS_MAP[pos] = i + 1

print(len(PRESENTS))
print(PRESENTS_MAP[:10, :10])