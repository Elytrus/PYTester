class Case:
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out
    
    def to_args(self):
        return self.inp, self.out

    def __str__(self):
        return 'input: %s, output: %s' % (self.inp, self.out)

# Helper Functions


# Returns Iterator of cases
def to_cases(inputs, outputs=None):
    if outputs:
        return [Case(inp, out) for inp, out in zip(inputs, outputs)]
    return [Case(inp, None) for inp in inputs]