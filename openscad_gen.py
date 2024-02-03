import random
import numpy as np
import sys

rng = np.random.default_rng()

d = float(sys.argv[1])
try:
    n = int(sys.argv[2])
except:
    n = 10

def scale(x, y, z):
    return f"scale([{x}, {y}, {z}])"

def translate(x, y, z):
    return f"translate([{x}, {y}, {z}])"

print("$fn = 100;")

for i in range(n):
    case = random.randint(0, 5)
    if case > 1:
        print(scale(rng.normal(0, 2), rng.normal(0, 2), rng.normal(0, 2)))
    print(translate(rng.normal(0, d), rng.normal(0, d), rng.normal(0, d)))
    print("cube(1);")
