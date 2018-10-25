import subprocess as sub
import time
from threading import Timer

TESTING_MODE = True


# Basic functions

def __decode_out(b):
    if b:
        return str(b, 'utf-8')
    return ''


def __parse_flags(f):
    if type(f) == list:
        return f
    return f.split(' ')


# Display Functions

def __process_output(out, err, tle, cor_out, flags):
    correct = False

    # Print Output
    if err:
        print('[ Errors ] : \n%s' % err)

    if 'disp_out' in flags:
        print('[ Output ] : \n%s' % out)

    if 'test' in flags:
        if tle:
            print('!! Time Limit Exceeded !!')
        elif out != cor_out:
            if 'disp_correct' in flags:
                print('[ Correct Solution (Output was Wrong!) ] :\n%s' % cor_out)
            else:
                print('!! Wrong Answer !!')
        else:
            print('!! Correct Answer !!')
            correct = True

    return correct


def __disp_input(inp, case_no, flags):
    # Show input
    if 'disp_in' in flags:
        print('-- Test Case #%d --\n[ Input ] : \n%s' % (case_no, inp))
    else:
        print('-- Test Case #%d --' % case_no)


def __test_file(file, inp, flags, time_limit, pre=None, post=None):
    # Open Subprocess
    proc = sub.Popen(['py', file], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)

    if pre:
        pre()

    # Send in Input and take back Output
    result = None
    tle = False
    ctime = time.time()

    def kproc():
        nonlocal tle, result
        proc.kill()
        tle = True
        result = ('', '')

    if 'check_time' in flags:
        try:
            timer = Timer(time_limit + 0.05, kproc)
            timer.start()
            result = proc.communicate(bytes(inp, 'utf-8'))
        finally:
            timer.cancel()
    else:
        result = proc.communicate(bytes(inp, 'utf-8'))

    out, err = map(__decode_out, result)

    if 'disp_time' in flags:
        elapsed = time.time() - ctime
        print('Case took %.3f seconds' % elapsed)

    if post:
        post()

    out = out.strip().replace('\r', '')

    return out, err, tle


'''
Valid flags for functions 'test_case' and 'test': 
test - Check input with output (Requires output argument to be filled)
disp_in - Display input
disp_out - Display output
disp_correct - Display correct output when output is wrong (Requires test flag)

disp_time - Display correct time
check_time - Checks whether time is within limits (Set the time_limit function parameter if you use this flag)
'''


def empty_fun():
    pass


def test_case(file, case, case_no, flags='', time_limit=None):
    flags = __parse_flags(flags)

    # Display Input
    __disp_input(case.inp, case_no, flags)

    results = __test_file(file, case.inp, flags, time_limit)

    # Display Output
    return __process_output(*results, case.out, flags)


def test(file, cases, flags='', time_limit=None):
    flags = __parse_flags(flags)
    case_count = len(cases)
    correct = 0

    print('-- [ Testing file %s with %d Test Cases ] --' % (file, case_count))

    if 'check_time' in flags:
        print(' -- The time limit for test  cases is %.2fs' % float(time_limit))

    print()

    for i, case in zip(range(1, case_count + 1), cases):
        correct += test_case(file, case, i, flags, time_limit)

        # Newline for Formatting
        print()

    if 'test' in flags:
        print('You got %d/%d cases correct!' % (correct, case_count))
        print('That was %.2f%% of all cases!' % (correct / case_count * 100))
