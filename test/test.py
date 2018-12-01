import os

from tester.handlers.text_handler import TextHandler
from tester.generators.util import *
from tester.generators.number import *
from tester.generators.graph import *

# Testing Functions

test_type = 'generator'
os.chdir('%s\\Desktop\\PYTester\\test' % (os.getenv('userprofile')))

if test_type == 'handler':
    tester = TextHandler()

    tester.test(open('iotest\\cases\\test_ir.ini'))  # IR Test

    tester.test(open('iotest\\cases\\test.ini'))  # Normal Test
    tester.test(open('iotest\\cases\\test_c.ini'))  # C Test
    tester.test(open('iotest\\cases\\test_cpp.ini'))  # CPP Test

    tester.test(open('iotest\\cases\\test_no_check_correct.ini'))  # No Correctness Test
    tester.test(open('iotest\\cases\\test_no_check_time.ini'))  # No Time Limit Test

    tester.test(open('iotest\\cases\\test_fast.ini'))  # WA Test

    tester.test(open('iotest\\cases\\test.ini'), True)  # Async Test

    print('random message here')
elif test_type == 'generator':
    lis = [[1, 2, 3,], [4, 5, 6], [7, 8, 9]]
    print(join_all(lis, '\n', ' '))

    g = TreeGenerator(5, increasing=False)
    print(g())

    g = GraphGenerator(10, 20, increasing=False)
    print(join_all(list(sorted(g())), '\n', ' '))

    print(join_all(WeightedGenerator(g, min_weight=10, max_weight=20)(), '\n', ' '))

    h = IncreasingSequenceGenerator(1, 100, 20, True)
    i = DecreasingSequenceGenerator(1, 100, 20, True)
    print(join_all(Repeater(Joiner(h, i), 10)(), '\n', ' '))
