import api.tester as ctest
import api.cases as cases

# Testing Functions

def test1(flags):
    ctest.test('echo.py', cases.to_cases(['test', 'test2', 'test3'], ['test', 'test2', 'this is not the right output']), flags)


def test2():
    ctest.test('badfile.py', ['test 1', 'test 2'])


test1('')
test1('disp_in disp_out')
test1('test')
test1('test disp_out')
test1('test disp_out disp_correct')
