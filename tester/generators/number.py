import random
from tester.generators.util import Joiner


class RandomGenerator:
    def __init__(self, left, right):
        self.min = left
        self.max = right

    def __call__(self):
        return random.randint(self.min, self.max)


class IncreasingSequenceGenerator:
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


class DecreasingSequenceGenerator(IncreasingSequenceGenerator):
    def __call__(self):
        return list(reversed(super().__call__()))


class NumberListGenerator(Joiner):
    def __init__(self, left, right, count=1):
        super().__init__(RandomGenerator(left, right), count)
