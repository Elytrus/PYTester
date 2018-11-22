import time
import os
import os.path
import subprocess as sub
from threading import Timer


def _create(command):
    """
    Creates subprocess with the command and pipes standard I/O streams

    :param command: The command to be passed into subprocess.Popen
    :type command: str
    :return: The process created
    """
    return sub.Popen(command, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)


def _create_py(file_name, argv):
    """
    Creates subprocess for python

    :param file_name: Name of Python File
    :return: The process created
    """

    return _create(['py', file_name] + argv)


def _create_nml(file_name, argv):
    """
    Creates subprocess for any executable file

    :param file_name: Name of executable file (.exe, .bat, etc.)
    :return: The process created
    """

    return _create([file_name] + argv)


def _pre_process_cpp(file_name):
    """
    Compiles the C++ source file

    :param file_name: Name of C++ Source file
    :return: The file name of the executable created
    """

    exec_name = '%s.exe' % os.path.splitext(file_name)[0]
    sub.call(['g++', '-o', exec_name, file_name])

    if not os.path.exists(exec_name):
        return 'CE'

    return exec_name


def _pre_process_c(file_name):
    """
    Compiles the C source file

    :param file_name: Name of C Source file
    :return: The file name of the executable created
    """

    exec_name = '%s.exe' % os.path.splitext(file_name)[0]
    sub.call(['gcc', '-o', exec_name, file_name])

    if not os.path.exists(exec_name):
        return 'CE'

    return exec_name


PRE_PROCESS = {
    '.cpp': _pre_process_cpp,
    '.c': _pre_process_c
}

CREATE_PROCESS = {
    '.py': _create_py,
    '.exe': _create_nml
}

POST_PROCESS = {
    '.exe': os.remove
}


def _decode_output(out_bytes):
    if out_bytes:
        return str(out_bytes, 'utf-8')
    return ''


def pre_exec_file(file_name):
    """
    Pre processes file, if the file name is changed, it will be returned

    :param file_name: The name of the file to be processed
    :return: The new file name if it changes, or None if it doesn't
    """

    ext = os.path.splitext(file_name)[1]

    if ext in PRE_PROCESS:
        return PRE_PROCESS[ext](file_name)


def post_exec_file(file_name):
    """
    Does any post execution of files after the test cases are finished

    :param file_name: The name of the file to be processed
    :return: None
    """

    ext = os.path.splitext(file_name)[1]

    if ext in POST_PROCESS:
        POST_PROCESS[ext](file_name)


def exec_file(file_name, case_input, time_limit=-1, argv=[]):
    """
    Executes a case for the file `file_name`

    :param argv: Optional system arguments to execute
    :param file_name: The name of the case to execute
    :param case_input: The test case input
    :param time_limit: The time limit in seconds, or -1 if there is no time limit
    :return: A tuple containing (in order) the output, any errors, whether there was a TLE, and the time elapsed
    """

    ext = os.path.splitext(file_name)[1]

    if ext in CREATE_PROCESS:
        process = CREATE_PROCESS[ext](file_name, argv)
    else:
        raise ValueError('Invalid file type!')

    tle = False
    begin_time = time.time()

    # Setting up timer and passing input

    def kill_process():
        nonlocal tle, result

        process.kill()
        tle = True
        result = ('', '')

    if time_limit != -1.0:
        try:
            timer = Timer(time_limit + 0.05, kill_process)
            timer.start()
            result = process.communicate(bytes(case_input, 'utf-8'))
        finally:
            timer.cancel()
    else:
        result = process.communicate(bytes(case_input, 'utf-8'))

    end_time = time.time()

    # Parsing output

    out, err = map(_decode_output, result)
    out = out.strip().replace('\r', '')

    return out, err, tle, end_time - begin_time
