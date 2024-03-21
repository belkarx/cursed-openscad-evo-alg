import random
import numpy as np
import sys
from pprint import pprint
import os
import pyperclip
from iterators import UniformRandomIter, FibIter, StableIter

rng = np.random.default_rng() #rng.normal(0, 1)

#random (normal(x, y))  
#exponential, log

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
# 2 because radius of sphere is 1
def cube():
    return "cube(2);"
#pyramid
#cylinder
#iterating polyhedra

def print_seed(seed):
    print()
    for part in seed:
        print("cube" if part['shape'] == cube else "sphere")
        print(part['number'])
        print(part['fn'])
        for transform in part['transforms']:
            print(f"  {transform['function'].__name__}")
            print(f"  {[g.__name__ for g in transform['generators']]}")
            print(f"  {transform['parameters']}")
            print("-")
        print()
    print()



# rotate is between 0 and 180 and should be relatively large
# translate - 1 to 3 for overlap, 1-5 for decent spread. can be negative
# scale - cant be 0, 1 the default, 1-3 variance is good

# scale fibiter by # of shapes

def new_seed_part():
    return {
        "shape": random.choice([sphere, cube]),
        "number": abs(int(rng.normal(10, 5))),
        "fn": abs(int(rng.normal(50, 10))),
        "transforms": [
            {
                "function": translate,
                "generators": [UniformRandomIter, UniformRandomIter, UniformRandomIter],
                "parameters": [[-3, 3, 1] for _ in range(3)],
                "iterators": [],
            },
            {
                "function": rotate,
                "generators": [StableIter for _ in range(3)],
                "parameters": [0 for _ in range(3)],
                "iterators": [],
            },
            {
                "function": scale,
                "generators": [StableIter for _ in range(3)],
                "parameters": [1 for _ in range(3)],
                "iterators": [],
            }


        ]
    }

def render(seed):
    print("RENDERING")
    to_paste = f"$fn = {seed[0]['fn']};\n"
    
    for part in seed:
        print(f"working on part with {part['number']} {part['shape']}s and {len(part['transforms'])} transforms""")
        for i in range(part["number"]):
            for transform in part["transforms"]:
                if transform["iterators"] == []:
                    init_iterators = [gen(p) for gen, p in 
                                      zip(transform["generators"], transform["parameters"])]
                    transform["iterators"] = init_iterators
                to_paste += transform["function"](*transform["iterators"]) + "\n"
            to_paste += part["shape"]() + "\n"

    #clearing iterators right after rendering
    for part in seed:
        for transform in part["transforms"]:
            transform["iterators"] = []
            

    print("RENDER?")
    input()
    print(to_paste)
    pyperclip.copy(to_paste)
    os.system("sh shopenscad.sh")

# change fn
# add, remove a transform
# change the iterator of a transform
# change parameters of iterator
# change number
# change shapev

seed = [new_seed_part()]
print_seed(seed)
render(seed)

def t_mutate(seed):
    for s in seed:
        for t in s["transforms"]:
            if t["function"] == translate:
                print("TRANSLATE MUTATED from ", t["parameters"])
                for i in range(3):
                    mut = [int(rng.normal(x, 2)) for x in t["parameters"][i][:2]]
                    mut.sort()
                    mut.append(1)
                    t["parameters"][i] = mut
                print("TRANSLATE MUTATED to ", t["parameters"])
    return seed

good = []
bad  = []

def mutate(good):
    new_good = []
    for g in good:
        new_good.append(random_mutate(g))
    return new_good

import copy
for i in range(20):
    seed = t_mutate(seed.copy())
    render(seed)
    if input() != "":
        print_seed(seed)
        good.append(copy.deepcopy(seed[0]["transforms"][0]["parameters"]))
    else:
        bad.append(copy.deepcopy(seed[0]["transforms"][0]["parameters"]))

with open("good.txt", "w") as f:
    f.write('\n'.join([str(x) for x in good]))
with open("bad.txt", "w") as f:
    f.write('\n'.join([str(x) for x in bad]))

input()

j = 0

while True:
    print("ITERATION: ", j)
    for s in seeds:
        render(s)

        i = input()
        if i != "":
            good.append(s.copy())
            if len(good) > 5:
                good.pop(0)
                print("removing from good")
        print("DONE RENDERING")

    seeds = []

    print("NUMBER OF SEEDS: ", len(good))
    for g in good:
        print_seed(g)
        print()
        new_seed = random_mutate(g)
        print("MUTATED SEED")
        print_seed(new_seed)
        seeds.append(new_seed)
