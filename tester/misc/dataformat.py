import os

IN_EXT = '.in'
OUT_EXT = '.out'

def format_for_dmoj(base_name, case_cnt):
    """
    Formats test cases for use on the DMOJ Online Judge (https://dmoj.ca)

    :param base_name: Base name of the test cases to be formatted
    :type base_name: str
    :param case_cnt: The amount of cases to format
    :type case_cnt: int
    :return: None
    """

    for i in range(1, case_cnt + 1):
        old = '%s_%d' % (base_name, i)
        new = '%s.%d' % (base_name, i)

        os.rename(old + IN_EXT, new + IN_EXT)
        os.rename(old + OUT_EXT, new + OUT_EXT)