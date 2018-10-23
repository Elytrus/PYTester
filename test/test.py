import api.tester as ctest
import api.cases as cases

# Testing Functions

def test1(flags):
    ctest.test('echo.py', cases.to_cases(['test', 'test2', 'test3'], ['test', 'test2', 'this is not the right output']), flags)


def test2():
    ctest.test('badfile.py', ['test 1', 'test 2'])


# test1('')
# test1('disp_in disp_out')
# test1('test')
# test1('test disp_out')
# test1('test disp_out disp_correct')
# test1('test disp_time')

io_cases = cases.parse_case_files('iotest/cases/echo', 1)

io_cases_sm = cases.parse_case_files('iotest/cases/echo_small', 1)
io_cases_lg = cases.parse_case_files('iotest/cases/echo_large', 1)

print('Loaded test input')

# ctest.test('iotest/echonormalio.py', io_cases, 'test disp_time')
# ctest.test('iotest/echonormalio.py', io_cases_lg, 'test disp_time')

ctest.test('iotest/echonormalio.py', io_cases, 'test disp_time check_time', 2)
ctest.test('iotest/echonormalio.py', io_cases_lg, 'test disp_time check_time', 2)