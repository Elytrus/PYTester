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


'''
Test Data File Format:

'=INPUT' - Denotes input cases
'=OUTPUT' - Denotes output cases
'--' - Denotes case separator

Example:

=INPUT
Hello, World!
--
Testing 2
=OUTPUT
Hell0, W0rld!
--
Testing 2

'''

DELIM_INPUT = '=INPUT\n'
DELIM_OUTPUT = '=OUTPUT\n'
DELIM_CASE = '--\n'


def parse_case_file(file_name):
    inputs = []
    outputs = []

    mode = 'in'
    curr_case = ''

    def push_case(curr_case):
        if curr_case != '':
            if mode == 'in':
                inputs.append(curr_case.strip())
            else:
                outputs.append(curr_case.strip())

    with open(file_name) as f:
        for line in f.readlines():
            if line == DELIM_INPUT or line == DELIM_OUTPUT or line == DELIM_CASE:
                push_case(curr_case)
                curr_case = ''

            if line == DELIM_INPUT:
                mode = 'in'
            elif line == DELIM_OUTPUT:
                mode = 'out'
            else:
                curr_case += line

    if curr_case != '':
        push_case(curr_case)

    return to_cases(inputs, outputs)
