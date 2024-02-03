import random
import numpy as np
import sys
from pprint import pprint
import os
import pyperclip

nrm = np.random.default_rng() #rng.normal(0, 1)

#itr1=number generator, governs complexity | stb (stable) uniform (incl 0), fibonacci (up to limit), random (normal(x, y)), random (uniform from x to y), exponential (up to limit), linear(1,5)
#itr2
#num=base number | 0-10 to start
#shp={shapes} | cube(1), sphere(1) to start
#tfm={transformations} | translate, scale, rotate to start

#itr-num#-itr-itr-shp-itr-itr-tfm

# trm implies (itr-itr-itr)
# itrtyp-itr implies itr-num# (as a limit)

#seed_cube = "10-mov-fib-MAX-stb-0-stb-0-rot-stb-0.5-stb-0.5-stb-0.5"#-scl-lin-0,5-lin-0,5-lin-0,5"

# iterators
class FibIter:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def next(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

class UniformRandomIter:
    def __init__(self, bottom_range, top_range):
        self.bottom = bottom_range
        self.top = top_range

    def __iter__(self):
        return self

    def next(self):
        return random.randint(self.bottom, self.top)

class StableIter:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def next(self):
        return self.value

# transforms
def scale(x, y, z):
    return f"scale([{x.next()}, {y.next()}, {z.next()}])"

def translate(x, y, z):
    return f"translate([{x.next()}, {y.next()}, {z.next()}])"

def rotate(x, y, z):
    return f"rotate([{x.next()}, {y.next()}, {z.next()}])"

# shapes
def sphere():
    return "sphere(1);"
def cube():
    return "cube(1);"


structure = [
    {
        "shape": sphere,
        "number": number,
        "fn": 100,
        "transforms": [
            {
                "function": translate,
                "parameters": [StableIter(0), StableIter(0), FibIter(number)],
            },
            {
                "function": rotate,
                "parameters": [StableIter(45), StableIter(45), FibIter(number)],
            },
            {
                "function": scale,
                "parameters": [UniformRandomIter(1, 5), UniformRandomIter(1, 5), UniformRandomIter(1, 5)],
            }
        ],
    }
]

def render(structure):
    to_paste = f"$fn = {structure[0]['fn']};\n"
    for shape in structure:
        for i in range(shape["number"]):
            for transform in shape["transforms"]:
                to_paste += transform["function"](*transform["parameters"]) + "\n"
                print(transform["function"](*transform["parameters"]))
            to_paste += shape["shape"]() + "\n"
            print(shape["shape"]())

    pyperclip.copy(to_paste)
    os.system("sh shopenscad.sh")

good = []
bad = []

# rlhf mutate loop

for i in range(5):
    render(structure)
    if input() != "":
        good.append(structure)
    else:
        bad.append(structure)

print(good)
print(bad)

def mutate(structure):
    # change fn
    # add, remove a transform
    # change the iterator of a transform
    # change parameters of iterator
    # change number
    # change shape
    pass
