import random
from tester.generators.util import Repeater


class RandomGenerator:
    def __init__(self, left, right):
        self.min = left
        self.max = right

    def __call__(self):
        return random.randint(self.min, self.max)


class IncreasingGenerator:
    def __init__(self, left, right, count, strict=False):
        self.strict = strict
        self.count = count
        self.max = right
        self.min = left

    def __call__(self):
        if self.strict:
            return sorted(random.sample(range(self.min, self.max), self.count))
        else:
            return sorted(random.choices(range(self.min, self.max), k=self.count))


class DecreasingGenerator(IncreasingGenerator):
    def __call__(self):
        return list(reversed(super().__call__()))


class NumberListGenerator(Repeater):
    def __init__(self, left, right, count=1):
        super().__init__(RandomGenerator(left, right), count)


"""
Aliases for the different generators
"""

rand = RandomGenerator
inc = IncreasingGenerator
dec = DecreasingGenerator