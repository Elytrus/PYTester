import builtin_handlers.text_handler as text_handler
import os

# Testing Functions

os.chdir('%s\\Desktop\\PYTester\\test' % (os.getenv('userprofile')))

tester = text_handler.TextHandler()

tester.test(open('iotest\\cases\\test_ir.ini'))  # IR Test

tester.test(open('iotest\\cases\\test.ini'))  # Normal Test
tester.test(open('iotest\\cases\\test_no_check_correct.ini'))  # No Correctness Test
tester.test(open('iotest\\cases\\test_no_check_time.ini'))  # No Time Limit Test

tester.test(open('iotest\\cases\\test_fast.ini'))  # WA Test

tester.test(open('iotest\\cases\\test.ini'), True) # Async Test

print('random message here')
