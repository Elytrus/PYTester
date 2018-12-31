import time
import os
import re
import shutil
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

def _create_java(file_name, argv):
    """
    Creates subprocess for any jar file

    :param file_name: Name of jar file
    :return: The process created
    """

    return _create(['java', '-jar', file_name] + argv)


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


JAR_MANIFEST = 'manifest.txt'


def _pre_process_java(file_name):
    """
    Compiles the Java source file

    :param file_name: Name of Java Source file
    :return: The file name of the executable created

    This shit is long as fuck
    """

    exec_name = '%s.jar' % os.path.splitext(file_name)[0]
    file_name_was_changed = False

    # Find public class

    with open(file_name) as f:
        source = f.read(os.path.getsize(file_name))

    match = re.search(r'public\s+class\s+(.*)\s*{', source, flags=re.MULTILINE)

    if not match:
        return 'CE'

    public_class = match.group(1).strip()
    new_name = '%s.java' % public_class

    if file_name != new_name:
        shutil.copy(file_name, new_name)
        file_name = new_name
        file_name_was_changed = True

    # Creating manifest and compiling source into class files

    with open(JAR_MANIFEST, 'w') as f:
        f.write('Main-Class: %s\n' % public_class)

    sub.call(['javac', file_name])

    # Finding Class file names

    class_files = []

    for file in os.listdir('.'):
        if os.path.splitext(file)[1] == '.class':
            print('filefile ', file)
            class_files.append('%s' % file)

    # Creating a jar file

    sub.call(['jar', 'cvfm', exec_name, JAR_MANIFEST] + class_files)

    # Cleanup work

    os.remove(JAR_MANIFEST)

    if file_name_was_changed:
        os.remove(file_name)

    for class_file in class_files:
        os.remove(class_file)

    # Return

    if not os.path.exists(exec_name):
        return 'CE'

    return exec_name


PRE_PROCESS = {
    '.cpp': _pre_process_cpp,
    '.c': _pre_process_c,
    '.java': _pre_process_java
}

CREATE_PROCESS = {
    '.py': _create_py,
    '.exe': _create_nml,
    '.jar': _create_java,
}

POST_PROCESS = {
    '.exe': os.remove,
    '.jar': os.remove
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
