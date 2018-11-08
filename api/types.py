class Case:
    def __init__(self, inp, out):
        """
        Constructs a api.types.Case object out of the following parameters

        :param inp: The input of the test case
        :type inp: str
        :param out: The output of the test case
        :type out: str
        """

        self.inp = inp
        self.out = out

    def to_args(self):
        """
        Converts the object into tuple form so that they can be unpacked for use in a loop, function, etc.

        :return: The input and output values of the test case as a tuple
        :rtype: tuple
        """

        return self.inp, self.out

    def __str__(self):
        """
        To string function

        :return: Self-explanatory
        :rtype: str
        """

        return 'input: %s, output: %s' % (self.inp, self.out)


class Result:
    def __init__(self, case_id, case, out, err, time, code):
        """
        Result constructor, creates an api.types.Result object with the following parameters

        :param case_id: The case number
        :type case_id: int
        :param case: The input + expected output of the test case
        :type case: api.types.Case
        :param out: The actual output of the case (from the program)
        :type out: str
        :param err: The errors from the case, or '' if there were none (from the program)
        :type err: str
        :param time: The amount of time it took for the code to execute
        :type time: float
        :param code: The code from the case (AC: Correct, WA: Wrong Answer, TLE: Time Limit Exceeded, IR: Error)
        :type code: str
        """

        self.case_id = case_id
        self.case = case
        self.out = out
        self.err = err
        self.time = time
        self.code = code
