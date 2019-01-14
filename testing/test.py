import os

from tester.handlers.text_handler import TextHandler
from tester.generators.util import *
from tester.generators.number import *
from tester.generators.graph import *
from testing.test_util import *

# Testing Functions

# Modes --
# handler: normal handler testing
# handler-java: java handler testing
# generator-number: number generator testing
# generator-graph: graph generator testing
# generator-graph-advanced: advanced graph generator testing

test_type = 'generator-graph-advanced'
os.chdir('%s\\Desktop\\PYTester\\testing' % (os.getenv('userprofile')))

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
elif test_type == 'handler-java':
    tester = TextHandler()

    tester.test(open('iotest\\cases\\test_java.ini'))  # Yava Test
elif test_type == 'generator-number':
    lis = [[1, 2, 3,], [4, 5, 6], [7, 8, 9]]
    print(join_all(lis, '\n', ' '))

    h = IncreasingGenerator(1, 100, 20, True)
    i = DecreasingGenerator(1, 100, 20, True)
    print(join_all(Repeater(Joiner(h, i), 10)(), '\n', ' '))
elif test_type == 'generator-graph':
    print('-- Tree test: --')
    g = TreeGenerator(5, increasing=False)
    print(g())

    print('-- Graph Test: --')
    g = GraphGenerator(10, 20, increasing=False)
    print(join_all(list(sorted(g())), '\n', ' '))

    print('-- Weighted Test: --')
    print(join_all(WeightedGenerator(g, min_weight=10, max_weight=20)(), '\n', ' '))
elif test_type == 'generator-graph-advanced':
    n = 20
    g = ConnectedGenerator(n, 50, allow_duplicate=False, increasing=False)

    random_test(graph_is_connected, [n, g], passes=100, show_inner_output=False)
    random_test(graph_has_self_loops, [g], passes=100, invert=True, show_inner_output=False)
    random_test(graph_has_duplicates, [g], passes=100, invert=True, show_inner_output=False)
