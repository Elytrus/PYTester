import api.tester as ctest


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

 -- Inputs:
<base_name>_<case #>.in

 -- Outputs:
<base_name>_<case #>.out

 -- Example:
<base_name> -> echo

echo_1.in
echo_2.in
echo_3.in
echo_1.out
echo_2.out
echo_3.out
'''


def parse_case_files(base_name, case_cnt=1):
    inputs = []
    outputs = []

    for i in range(1, case_cnt + 1):
        curr_base_name = '%s_%d' % (base_name, i)

        with open('%s.in' % curr_base_name, 'r') as f:
            inputs.append(f.read())

        with open('%s.out' % curr_base_name, 'r') as f:
            outputs.append(f.read())

    return to_cases(inputs, outputs)


def test_all_cases(base_name, prgm_file, flags, case_cnt=1):
    ctest.test(prgm_file, parse_case_files(base_name, case_cnt), flags)
