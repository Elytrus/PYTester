import subprocess as sub
import time

TESTING_MODE = True


# Basic functions

def __decode_out(b):
    if b:
        return str(b, 'utf-8')
    return 0


def __parse_flags(f):
    if type(f) == list:
        return f
    return f.split(' ')


# Display Functions

def __disp_output(out, err, cor_out, flags):
    # Print Output
    if err:
        print('[ Errors ] : \n%s' % err)

    if 'disp_out' in flags:
        print('[ Output ] : \n%s' % out)

    if 'test' in flags:
        if out != cor_out:
            if 'disp_correct' in flags:
                print('[ Correct Solution (Output was Wrong!) ] :\n%s' % cor_out)
            else:
                print('!! Wrong Answer !!')
        else:
            print('!! Correct Answer !!')


def __disp_input(inp, case_no, flags):
    # Show input
    if 'disp_in' in flags:
        print('-- Test Case #%d --\n[ Input ] : \n%s' % (case_no, inp))
    else:
        print('-- Test Case #%d --' % case_no)


def __test_file(file, inp, pre=None, post=None):
    # Open Subprocess
    proc = sub.Popen(['py', file], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)

    if pre:
        pre()

    # Send in Input and take back Output
    out, err = map(__decode_out, proc.communicate(bytes(inp, 'utf-8')))

    if post:
        post()

    out = out.strip().replace('\r', '')

    return out, err


'''
Valid flags for functions 'test_case' and 'test': 
test - Check input with output (Requires output argument to be filled)
disp_in - Display input
disp_out - Display output
disp_correct - Display correct output when output is wrong (Requires test flag)

disp_time - Display correct time
'''


def empty_fun():
    pass


def test_case(file, case, case_no, flags=''):
    flags = __parse_flags(flags)

    # Display Input
    __disp_input(case.inp, case_no, flags)

    def new_time():
        print('Case took %.3f seconds' % (time.time() - ctime))

    ctime = time.time()
    out, err = __test_file(file, case.inp, post=new_time if 'disp_time' in flags else empty_fun)

    # Display Output
    __disp_output(out, err, case.out, flags)


def test(file, cases, flags=''):
    flags = __parse_flags(flags)
    case_count = len(cases)

    print('-- [ Testing file %s with %d Test Cases ] --' % (file, case_count))
    for i, case in zip(range(1, case_count + 1), cases):
        test_case(file, case, i, flags)

        # Newline for Formatting
        print()