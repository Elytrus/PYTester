from collections import namedtuple


class Case:
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out

    def to_args(self):
        return self.inp, self.out

    def __str__(self):
        return 'input: %s, output: %s' % (self.inp, self.out)


Results = namedtuple('Results', 'cases out time code')
