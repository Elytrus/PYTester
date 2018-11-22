import os

from tester.handlers.text_handler import TextHandler

# Testing Functions

os.chdir('%s\\Desktop\\PYTester\\test' % (os.getenv('userprofile')))

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
