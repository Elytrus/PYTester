import builtin.text_handler as text_handler
import os

# Testing Functions

os.chdir('C:\\Users\\2021100\\Desktop\\PYTester\\test')

print(os.listdir(os.getcwd()))

tester = text_handler.TextHandler()
tester.test(open('iotest\\cases\\test.ini'))
