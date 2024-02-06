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
    def __init__(self, scale=1):
        self.a, self.b = 0, scale*1

    def __iter__(self):
        return self

    def next(self):
        result = self.a
        self.a, self.b = self.b, (self.a + self.b)
        return result

    def reset(self):
        self.a, self.b = 0, 1

    def __str__(self):
        return "FibIter"
    def __repr__(self):
        return "FibIter"

class DropN:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def next(self):
        if i % self.n == 0:
            return 0
        return 1

class UniformRandomIter:
    def __init__(self, rnge):
        self.bottom = rnge[0]
        self.top = rnge[1]
        self.scale = rnge[2]

    def __iter__(self):
        return self

    def next(self):
        return random.randint(self.bottom, self.top) * self.scale

    def __str__(self):
        return "UniformRandomIter"
    def __repr__(self):
        return "UniformRandomIter"

class StableIter:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def next(self):
        return self.value

    def __str__(self):
        return "StableIter"
    def __repr__(self):
        return "StableIter"

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

seeds = [
    [
        {
            "shape": sphere,
            "number": 10,
            "fn": 50,
            "transforms": [
                {
                    "function": translate,
                    "generators": [StableIter, StableIter, FibIter],
                    "parameters": [0, 0, 1],
                    "iterators": [],
                },
                {
                    "function": rotate,
                    "generators": [StableIter, StableIter, FibIter],
                    "parameters": [45, 45, 1],
                    "iterators": [],
                },
                {
                    "function": scale,
                    "generators": [
                        UniformRandomIter,
                        UniformRandomIter,
                        UniformRandomIter,
                    ],
                    "parameters": [[1, 5], [1, 5], [1, 5]],
                    "iterators": [],
                },
            ],
        },
        {
            "shape": cube,
            "number": 1,
            "fn": 50,
            "transforms": [
                {
                    "function": translate,
                    "generators": [StableIter, StableIter, StableIter],
                    "parameters": [0, 0, 0],
                    "iterators": [],
                },
            ],
        }

    ]
]

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
                "parameters": [[-3, 3, 1], [-3, 3, 1], [-3, 3, 1]],
                "iterators": [],
            },
            {
                "function": rotate,
                "generators": [StableIter for _ in range(3)],
                "parameters": [0 for _ in range(3)]],
                "iterators": [],
            },
            {
                "function": scale,
                "generators": [StableIter for _ in range(3)],
                "parameters": [0 for _ in range(3)]],
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
            #print("CHECKING IF INSTANTIATED")
            #print(transform["generators"])
            #print(transform["iterators"])
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
input()
render(seed)
input()

def random_mutate(structure):
    print("mutating")

    for s in structure:
        #mutate fn
        #s['fn'] = abs(int(rng.normal(s['fn'], 50)))

        #mutate number
        print("number mutated from ", s['number'], end=" ")
        s['number'] = abs(int(rng.normal(s['number'], 5)))
        print("to ", s['number'])

        # mutate shape
        if random.random() < 0.1:
            s['shape'] = random.choice([sphere, cube])
            print("shape mutated")

        # add transform
        for t in s['transforms']:
            #mutate transform
            for i in range(3):
                #change generator
                if random.random() < 0.2:
                     print("generator mutated from ", t['generators'][i], end=" ")
                    t['generators'][i] = random.choice([UniformRandomIter, FibIter, StableIter])
                    print("to ", t['generators'][i])

                if t['generators'][i] == UniformRandomIter:
                        t['parameters'][i] = sorted([abs(int(rng.normal(5, 1))) for _ in range(2)])
                elif t['generators'][i] == FibIter:
                        # scale by some random number
                        t['parameters'][i] = abs(int(rng.normal(1, 5))*.1)
                elif t['generators'][i] == StableIter:
                        t['parameters'][i] = abs(int(rng.normal(2, 1)))

            #make sure to clear iterators (not necessary bc render? no that does that after)
            t['iterators'] = []

        # do some limit checks on parameters?

    return structure

def mutate(good):
    new_good = []
    for g in good:
        new_good.append(random_mutate(g))
    return new_good

good = []

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
