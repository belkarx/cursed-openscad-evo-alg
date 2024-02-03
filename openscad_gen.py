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

fib = FibonacciIter(10)
nrm = np.random.default_rng() #rng.normal(0, 1)


#itr=number generator, governs complexity | uniform, 0, fibonacci, random (normal(x, y)), exponential
#num=base number | 0-10 to start
#shp={shapes} | cube, sphere to start
#tfm={transformations} | translate, scale, rotate to start

#itr-num-itr-itr-shp-itr-itr-tfm


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
