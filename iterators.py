import random

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

