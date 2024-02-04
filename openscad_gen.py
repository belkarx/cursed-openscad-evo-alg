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
        self.a, self.b = 0, .1

    def __iter__(self):
        return self

    def next(self):
        result = self.a
        self.a, self.b = self.b, (self.a + self.b)
        return result

    def reset(self):
        self.a, self.b = 0, 1

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

        #make sure to reset fibonnaci iterator
        for transform in shape["transforms"]:
            for itr in transform["parameters"]:
                if isinstance(itr, FibIter):
                    itr.reset()
    #print(to_paste)
    pyperclip.copy(to_paste)
    os.system("sh shopenscad.sh")

# change fn
# add, remove a transform
# change the iterator of a transform
# change parameters of iterator
# change number
# change shapev

def mutate(structure, good):
    print("mutating")

    for s in structure:
        #mutate fn
        #s['fn'] = abs(int(rng.normal(s['fn'], 50)))

        #mutate number
        s['number'] = abs(int(rng.normal(s['number'], 5)))

        #mutate transforms
        for t in s['transforms']:
            if random.random() < 0.2:
                #mutate transform
                for i in range(3):
                    if random.random() < 0.07:
                        t['function'] = random.choice([scale, translate, rotate])
                    if random.random() < 0.3:
                        t['parameters'][i] = random.choice([UniformRandomIter(0, 5), FibIter(), StableIter(rng.normal(0, 3))])

        if random.random() < 0.05:
                #remove a transform
                s['transforms'].remove(t)

        # mutate shape
        if random.random() < 0.1:
            s['shape'] = random.choice([sphere, cube])
    
    return structure


good = []

j = 0

while True:
    print("ITERATION: ", j)
    for s in seeds:
        render(s)

        i = input()
        if i != "":
            if i == "s":
                print(good)
            good.append(s.copy())
            if len(good) > 5:
                good.pop(0)
        print("DONE RENDERING")

    seeds = []

    print("NUMBER OF SEEDS: ", len(good))
    for g in good:
        print(g)
        print()
        new_seed = mutate(g, good)
        print(new_seed)
        seeds.append(new_seed)
