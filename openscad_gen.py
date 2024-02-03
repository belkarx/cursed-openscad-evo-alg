import random
import numpy as np
import sys
from pprint import pprint
import os
import pyperclip

rng = np.random.default_rng() #rng.normal(0, 1)

#random (normal(x, y))  
#exponential, log

# iterators
class FibIter:
    def __init__(self, limit=None):
        #limit exists just for Compatibility
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def next(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

    def reset(self):
        self.a, self.b = 0, 1

class UniformRandomIter:
    def __init__(self, rnge):
        self.bottom = rnge[0]
        self.top = rnge[1]

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


seeds = [[
    {
        "shape": sphere,
        "number": 10,
        "fn": 50,
        "transforms": [
            {
                "function": translate,
                "generators": [StableIter, StableIter, FibIter],
                "parameters": [0, 0, None],
            },
            {
                "function": rotate,
                "generators": [StableIter, StableIter, FibIter],
                "parameters": [45, 45, None],
            },
            {
                "function": scale,
                "generators": [UniformRandomIter, UniformRandomIter, UniformRandomIter],
                "parameters": [[1, 5], [1, 5], [1, 5]],
            }
        ],
    }
]]

f = FibIter()

def render(structure):
    to_paste = f"$fn = {structure[0]['fn']};\n"

    for shape in structure:
        for i in range(shape["number"]):
            for transform in shape["transforms"]:
                to_paste += transform["function"](*[generator(parameter) for generator, parameter in zip(transform["generators"], transform["parameters"])]) + "\n"

                for g in transform["generators"]:
                    if g == FibIter:
                        g = f
            to_paste += shape["shape"]() + "\n"


    print(to_paste)
    pyperclip.copy(to_paste)
    os.system("sh shopenscad.sh")

# change fn
# add, remove a transform
# change the iterator of a transform
# change parameters of iterator
# change number
# change shapev

def mutate(structure, good, bad):
    print("mutating")
    for s in structure:
        s['fn'] = abs(int(rng.normal(s['fn'], 50)))
    return structure


good = []
bad = []

for s in seeds:
    render(s)
    if input() != "":
        good.append(s.copy())
    print("DONE RENDERING")
    #else:
    #    bad.append(structure.copy())

for g in good:
    print(g)
    print()
    new_seed = mutate(g.copy(), good, bad)
    print(new_seed)
    render(new_seed)
    
    print()
    print("----")
