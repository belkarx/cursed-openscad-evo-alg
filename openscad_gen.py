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
    def __init__(self):
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


seeds = [[
    {
        "shape": sphere,
        "number": 10,
        "fn": 50,
        "transforms": [
            {
                "function": translate,
                "parameters": [StableIter(0), StableIter(0), FibIter()],
            },
            {
                "function": rotate,
                "parameters": [StableIter(45), StableIter(45), FibIter()],
            },
            {
                "function": scale,
                "parameters": [UniformRandomIter(1, 5), UniformRandomIter(1, 5), UniformRandomIter(1, 5)],
            }
        ],
    }
]]

def render(structure):
    to_paste = f"$fn = {structure[0]['fn']};\n"

    for shape in structure:
        for i in range(shape["number"]):
            for transform in shape["transforms"]:
                to_paste += transform["function"](*transform["parameters"]) + "\n"
                #print(transform["function"](*transform["parameters"]))
            to_paste += shape["shape"]() + "\n"
            #print(shape["shape"]())

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
    new_seed = mutate(g, good, bad)
    print(new_seed)
    render(new_seed)
    
    print()
    print("----")
