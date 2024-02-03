import random
import numpy as np
import sys

class FibonacciIter:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.a > self.limit:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

class UniformRandomIter:
    def __init__(self, bottom_range, top_range):
        self.bottom = bottom_range
        self.top = top_range

    def __iter__(self):
        return self

    def __next__(self):
        return random.randint(self.bottom, self.top)

class StableIter:
    def __init__(self, limit):
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        return self.limit

nrm = np.random.default_rng() #rng.normal(0, 1)

#itr1=number generator, governs complexity | stb (stable) uniform (incl 0), fibonacci (up to limit), random (normal(x, y)), random (uniform from x to y), exponential (up to limit), linear(1,5)
#itr2
#num=base number | 0-10 to start
#shp={shapes} | cube(1), sphere(1) to start
#tfm={transformations} | translate, scale, rotate to start

#itr-num#-itr-itr-shp-itr-itr-tfm

# trm implies (itr-itr-itr)
# itrtyp-itr implies itr-num# (as a limit)

def scale(x, y, z):
    return f"scale([{x.next()}, {y.next()}, {z.next()}])"

def translate(x, y, z):
    return f"translate([{x.next()}, {y}, {z}])"

def rotate(x, y, z):
    return f"rotate([{x}, {y}, {z}])"

print("$fn = 100;")

# 10 shapes, 10 cubes then 10 spheres, cubes transformed up according to fibonacci sequence (scaled by .5) and rotated uniformly by 1, scaled by linear random generator, spheres translated to left by 1 each
seed_cube = "10-mov-fib-MAX-stb-0-stb-0-rot-stb-0.5-stb-0.5-stb-0.5"#-scl-lin-0,5-lin-0,5-lin-0,5"

seed_cube = seed_cube.split("-")

n_shapes = int(seed_cube[0])


def get_number_gen(number_gen, seed_cube):
    if number_gen == "fib":
        return FibonacciIter(seed_cube.next())
    elif number_gen == "stb":
        return StableIter(seed_cube.next())

trfm_generators = [shapes_to_act_on_number_and_type: [functions:[parameters]]]

def sphere():
    return "sphere(1);"

structure = [{"shape":sphere(), number: 10, transforms:[translate(StableIter(0), StableIter(0), FibonacciIter(number)), rotate(Stable(0.5), StableIter(0.5), StableIter(0.5), scale(UniformRandomIter(0, 5), UniformRandomIter(0,5), UniformRandomIter(0,5)]}]

for cdn in seed_cube:
    if cdn in ["mov", "rot", "scl"]:
        if cdn == "mov":
            transform = translate()
            continue
        elif cdn == "rot"
            transform = rotate()
            continue
        elif cdn == "scl"
            transform = scale()
            continue
    
        generator = seed_cube.next()
        if generator in ["fib", "stb"]:
            number_gen_1 = get_number_gen(generator, seed_cube)
            number_gen_2 = get_number_gen(seed_cube.next(), seed_cube)
            number_gen_3 = get_number_gen(seed_cube.next(), seed_cube)
        
            print(transform(number_gen_1.next(), number_gen_2.next(), number_gen_3.next()))
